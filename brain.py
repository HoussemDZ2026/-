import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class FutureSetBrain:
    def __init__(self):
        # السيرفر راح يقرأ المفتاح من إعدادات البيئة
        api_key = os.getenv("GOOGLE_API_KEY")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key
        )
        
        self.system_prompt = """
        أنت المساعد الذكي المتخصص لمنصة 'Future Set' التعليمية.
        مهمتك هي مساعدة المستخدم في تصميم الإعلانات والسيناريوهات بلهجة جزائرية بيضاء أو فصيحة.
        دائماً ركز على فوائد التعليم، المستقبل، والاحترافية التي تقدمها منصة Future Set.
        """

    def get_response(self, user_query):
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("user", "{query}")
            ])
            chain = prompt | self.llm | StrOutputParser()
            return chain.invoke({"query": user_query})
        except Exception as e:
            return f"خطأ في معالجة الطلب: {str(e)}"

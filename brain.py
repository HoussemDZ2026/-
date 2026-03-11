import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

class FutureSetBrain:
    def __init__(self):
        # إعداد نموذج Gemini 1.5 Flash (سريع واقتصادي وممتاز للهاتف)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # تعليمات النظام لضبط هوية التطبيق
        self.system_prompt = """
        أنت المساعد الذكي المتخصص لمنصة 'Future Set' التعليمية.
        مهمتك هي مساعدة المستخدم في تصميم الإعلانات.
        
        يجب أن تلتزم بالقواعد التالية:
        1. إذا طلب المستخدم (نص إعلاني): اكتب نصاً تسويقياً جذابة بلهجة جزائرية بيضاء أو عربية فصيحة.
        2. إذا طلب المستخدم (صورة): قم بوصف مشهد إعلاني احترافي يمكن استخدامه كمطالبة (Prompt) لمولد صور.
        3. إذا طلب المستخدم (فيديو): اكتب سيناريو قصير (Script) مقسم لثواني.
        
        دائماً ركز على فوائد التعليم، المستقبل، والاحترافية التي تقدمها منصة Future Set.
        """

    def get_response(self, user_query):
        # بناء القالب (Template)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{query}")
        ])
        
        # ربط المكونات (Chain)
        chain = prompt | self.llm | StrOutputParser()
        
        # تنفيذ الطلب
        return chain.invoke({"query": user_query})

# الجزء الخاص بتجربة الكود مباشرة في Pydroid 3
if __name__ == "__main__":
    brain = FutureSetBrain()
    print("--- اختبار العقل الذكي لفيوتر سيت ---")
    test_input = "حاب ندير إعلان لدورة الرياضيات للباك"
    print(f"السؤال: {test_input}")
    print(f"الرد:\n{brain.get_response(test_input)}")

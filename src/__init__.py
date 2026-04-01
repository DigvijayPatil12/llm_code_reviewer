def __init__(self):
        # The Panel of Experts (Updated to the Gemini 2.5 series!)
        # Using 2.5 Pro for complex reasoning and context
        self.logic_expert = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.1)
        self.context_expert = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)
        
        # Using 2.5 Flash for faster, focused tasks
        self.security_expert = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
        
        # The Lead Reviewer
        self.synthesis_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
from langchain.prompts import PromptTemplate

class ResumeProcessor:
    def __init__(self, llm_model):
        self.llm_model = llm_model
    
    def analyze_resume(self, resume):
        """Analyze the resume and extract details."""
        prompt_template = """
        You are an expert resume reviewer. Analyze the following resume by extracting the candidate’s skills, work experience, education, and achievements.
        Provide a detailed breakdown of the resume and suggest improvements.

        Here is the resume:
        {resume}
        """
        prompt = PromptTemplate(input_variables=["resume"], template=prompt_template).format(resume=resume)
        return self.llm_model.query(prompt)

    def match_job_description(self, resume, job_description):
        """Match the resume with the job description and highlight missing skills."""
        prompt_template = """
        Match the following job description to this resume. Highlight the relevant skills and experience in the resume, and list any missing qualifications or skills that the candidate needs to meet the job requirements.

        Job Description:
        {job_description}

        Resume:
        {resume}
        """
        prompt = PromptTemplate(input_variables=["job_description", "resume"], template=prompt_template).format(
            job_description=job_description, resume=resume
        )
        return self.llm_model.query(prompt)

    def improve_resume(self, resume):
        """Improve the resume by enhancing clarity, grammar, and tone."""
        prompt_template = """
        Improve the following resume by enhancing clarity, grammar, and professional tone. Focus on making the descriptions impactful and concise.

        Here is the resume:
        {resume}
        """
        prompt = PromptTemplate(input_variables=["resume"], template=prompt_template).format(resume=resume)
        return self.llm_model.query(prompt)

    def suggest_career_path(self, resume):
        """Provide career path suggestions based on the resume."""
        prompt_template = """
        Based on the following resume and the candidate's experience, suggest a career path. Identify the skills and experiences the candidate should focus on to achieve their career goals.

        Here is the resume:
        {resume}
        """
        prompt = PromptTemplate(input_variables=["resume"], template=prompt_template).format(resume=resume)
        return self.llm_model.query(prompt)


class ResumeEnhancementPipeline:
    def __init__(self, llm_model):
        self.resume_processor = ResumeProcessor(llm_model)

    def process_resume(self, resume, job_description=None):
        # Step 1: Analyze resume
        analysis_result = self.resume_processor.analyze_resume(resume)
        print("Resume Analysis:\n", analysis_result)

        # Step 2: Match with job description (if provided)
        if job_description:
            job_match_result = self.resume_processor.match_job_description(resume, job_description)
            print("\nJob Match Result:\n", job_match_result)

        # Step 3: Improve the resume
        improved_resume = self.resume_processor.improve_resume(resume)
        print("\nImproved Resume:\n", improved_resume)

        # Step 4: Suggest career path
        career_path_suggestions = self.resume_processor.suggest_career_path(resume)
        print("\nCareer Path Suggestions:\n", career_path_suggestions)

        return {
            "analysis": analysis_result,
            "job_match": job_match_result if job_description else None,
            "improved_resume": improved_resume,
            "career_suggestions": career_path_suggestions,
        }

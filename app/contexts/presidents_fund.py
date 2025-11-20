import difflib

def get_faq_answer(user_question: str) -> str:
    """
    Returns the best matching FAQ answer for a user's question.
    Provides a concise, clear answer. If no good match, returns None.
    """
    faqs = CONTEXT["faqs"]
    # Find best match using difflib
    questions = [faq["question"] for faq in faqs]
    match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.6)
    if match:
        for faq in faqs:
            if faq["question"] == match[0]:
                # Prefer a single answer, else return only the first answer for multi-answer FAQs
                if "answer" in faq:
                    return faq["answer"]
                elif "answers" in faq:
                    return faq["answers"][0]
    return "Sorry, I couldn't find an exact answer. Please contact the President's Fund for more information."
CONTEXT = {
    "system_prompt": "You are an AI assistant for the President's Fund of Sri Lanka. Your role is to provide accurate information about medical assistance, eligibility, and the application process.",
    "context_info": "Find answers to the most common questions about applying for medical assistance, eligibility, and the application process.",
    "faqs": [
        {"question": "Do the applicants need to visit the Colombo office to obtain medical assistance from the President's Fund?", "answer": "No, the applicants now can submit their applications to the nearest Divisional Secretariat."},
        {"question": "How to obtain an application?", "answers": ["Through the website of the President's Fund (www.presidentsfund.gov.lk)", "Through Whatsapp (sending a message to Whatsapp no 0740854527)", "By visiting the nearest Divisional Secretariat", "By visiting the President's Fund", "Through mail (sending a request letter to the President's Fund)"]},
        {"question": "Whether the patient has to be the applicant?", "answers": ["No, a family member can apply instead of the patient", "In the event of no family member to represent, a closest relation can apply for the patient"]},
        {"question": "Whether the application can only be made before the surgery?", "answer": "No, the applications can be submitted within 60 days from the date of discharge from the hospital after the surgery or treatment (including weekends and public holidays)."},
        {"question": "Whether it is possible to reimburse the total amount spent for the surgery?", "answer": "No, please refer this link for more details on the amount given for the surgery or treatment."},
        {"question": "Is it compulsory to submit the original copies of the bills when applying?", "answer": "Yes, it is compulsory to submit the originals of the bills and receipts issued by the relevant institutions when applying for medical assistance."},
        {"question": "Whether it is possible to apply for medical assistance, in case of reimbursement from other institutions?", "answers": ["Receiving reimbursement from other institutions (ex: Agrahara, insurance company) is not an obstacle for applying", "The President's Fund will not grant medical assistance in case of covering 50% of medical expenses or more from such institutions in relevant to the expenses of the surgery or treatment."]},
        {"question": "Whether the public officers are not eligible to submit applications?", "answer": "No, even the public officers are eligible to apply for medical assistance from the President's Fund."},
        {"question": "Whether an applicant who received medical assistance once, is eligible to re-apply?", "answer": "Yes, application can be made in three instances and medical assistance can be received up to maximum 1 million."},
        {"question": "Whether the applications can be made for surgeries conducted in government hospitals?", "answers": ["No, no payment is made for the surgeries conducted in government hospitals", "The applications can be submitted for the list of diseases and for purchasing equipment from other institutions mentioned in the government hospitals in approved list of diseases, subject to the approved provisions."]},
        {"question": "How long will it take to make the payments?", "answer": "If there is no other special reason and if the patient has duly submitted the application with all the documents, the payment period may be around 3 to 5 days."},
        {"question": "Who will be paid in case the patient died or become immobilized?", "answer": "A decision is taken after obtaining a comprehensive report along with the recommendation from the Divisional or District Secretary."}
    ]
}

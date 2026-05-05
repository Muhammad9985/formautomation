import random
from typing import Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class Persona:
    """A consistent set of user data for a single form submission."""
    name: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    age: int = 0
    gender: str = ""
    company: str = ""
    job_title: str = ""
    department: str = ""
    education: str = ""
    experience: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "age": str(self.age),
            "gender": self.gender,
            "company": self.company,
            "job_title": self.job_title,
            "department": self.department,
            "education": self.education,
            "experience": self.experience
        }


class FormContext(Enum):
    MEDICAL = "medical"
    IT_TECH = "it_tech"
    EDUCATION = "education"
    BUSINESS = "business"
    EVENT = "event"
    SURVEY = "survey"
    JOB_APPLICATION = "job_application"
    FEEDBACK = "feedback"
    REGISTRATION = "registration"
    ORDER = "order"
    CONTACT = "contact"
    GENERAL = "general"


@dataclass
class FormProfile:
    context: FormContext
    topic: str
    industry: str
    formality_level: str  # formal, casual, mixed
    primary_language: str  # english, local, mixed
    detected_keywords: list[str]


class FormAnalyzer:
    """Analyzes form title and fields to determine context and generate appropriate data."""

    CONTEXT_KEYWORDS = {
        FormContext.MEDICAL: [
            "medical", "health", "hospital", "doctor", "patient", "nurse", "clinic",
            "pharmacy", "medicine", "surgery", "diagnosis", "treatment", "symptom",
            "vaccination", "covid", "virus", "disease", "therapy", "dental", "eye",
            "cardiologist", "dermatologist", "pediatric", "emergency", "ambulance"
        ],
        FormContext.IT_TECH: [
            "software", "programming", "developer", "engineer", "tech", "it ", "computer",
            "website", "app", "application", "code", "data", "cloud", "cyber", "network",
            "database", "ai", "artificial intelligence", "machine learning", "devops",
            "frontend", "backend", "fullstack", "api", "javascript", "python", "java"
        ],
        FormContext.EDUCATION: [
            "school", "university", "college", "student", "teacher", "professor",
            "course", "class", "grade", "homework", "exam", "test", "education",
            "learning", "study", "degree", "diploma", "certificate", "academic",
            "tuition", "scholarship", "admission", "enrollment"
        ],
        FormContext.BUSINESS: [
            "business", "company", "corporate", "office", "employee", "employer",
            "manager", "ceo", "director", "finance", "accounting", "marketing",
            "sales", "hr", "human resources", "payroll", "budget", "revenue",
            "client", "customer", "vendor", "supplier", "meeting", "conference"
        ],
        FormContext.EVENT: [
            "event", "party", "wedding", "birthday", "conference", "seminar",
            "workshop", "webinar", "meetup", "gathering", "celebration", "festival",
            "concert", "show", "exhibition", "trade show", "summit", "retreat",
            "rsvp", "invitation", "guest", "attendee", "speaker", "organizer"
        ],
        FormContext.SURVEY: [
            "survey", "poll", "questionnaire", "feedback", "opinion", "rate",
            "rating", "review", "satisfaction", "experience", "how would you",
            "what do you think", "tell us about", "your thoughts", "evaluate"
        ],
        FormContext.JOB_APPLICATION: [
            "job", "career", "position", "hiring", "recruitment", "apply",
            "application", "resume", "cv", "interview", "qualification",
            "experience", "skill", "candidate", "employment", "work",
            "salary", "wage", "benefits", "cover letter"
        ],
        FormContext.FEEDBACK: [
            "feedback", "complaint", "suggestion", "review", "comment",
            "improvement", "issue", "problem", "satisfaction", "dissatisfied",
            "excellent", "terrible", "awesome", "poor", "quality", "service"
        ],
        FormContext.REGISTRATION: [
            "register", "sign up", "join", "membership", "account", "subscribe",
            "newsletter", "enroll", "booking", "reservation", "appointment",
            "schedule", "confirm", "confirmation"
        ],
        FormContext.ORDER: [
            "order", "purchase", "buy", "product", "item", "cart", "checkout",
            "payment", "shipping", "delivery", "invoice", "receipt", "quantity",
            "price", "cost", "total", "discount", "coupon"
        ],
        FormContext.CONTACT: [
            "contact", "message", "inquiry", "question", "reach", "get in touch",
            "support", "help", "info", "information", "query", "request"
        ]
    }

    @classmethod
    def analyze_form(cls, form_title: str, field_labels: list[str]) -> FormProfile:
        """Analyze form title and field labels to determine context."""
        all_text = f"{form_title} {' '.join(field_labels)}".lower()

        # Count keyword matches for each context
        context_scores = {}
        detected_keywords = []

        for context, keywords in cls.CONTEXT_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                count = all_text.count(keyword)
                if count > 0:
                    score += count
                    detected_keywords.append(keyword)
            context_scores[context] = score

        # Determine primary context
        if not context_scores or max(context_scores.values()) == 0:
            primary_context = FormContext.GENERAL
        else:
            primary_context = max(context_scores.items(), key=lambda x: x[1])[0]

        # Determine topic from title
        topic = form_title.strip() if form_title else "General Form"

        # Determine industry
        industry = cls._determine_industry(primary_context, all_text)

        # Determine formality level
        formality_level = cls._determine_formality(all_text)

        # Determine language
        primary_language = "english"  # Default, can be extended

        return FormProfile(
            context=primary_context,
            topic=topic,
            industry=industry,
            formality_level=formality_level,
            primary_language=primary_language,
            detected_keywords=list(set(detected_keywords))
        )

    @classmethod
    def _determine_industry(cls, context: FormContext, all_text: str) -> str:
        """Determine specific industry based on context and text."""
        industry_map = {
            FormContext.MEDICAL: "Healthcare",
            FormContext.IT_TECH: "Technology",
            FormContext.EDUCATION: "Education",
            FormContext.BUSINESS: "Business",
            FormContext.EVENT: "Event Management",
            FormContext.SURVEY: "Research",
            FormContext.JOB_APPLICATION: "Human Resources",
            FormContext.FEEDBACK: "Customer Service",
            FormContext.REGISTRATION: "Administration",
            FormContext.ORDER: "E-commerce",
            FormContext.CONTACT: "Support",
            FormContext.GENERAL: "General"
        }
        return industry_map.get(context, "General")

    @classmethod
    def _determine_formality(cls, all_text: str) -> str:
        """Determine formality level of the form."""
        formal_indicators = ["dear", "sincerely", "respectfully", "application", "official", "formal"]
        casual_indicators = ["hey", "cool", "awesome", "fun", "chill", "hangout"]

        formal_count = sum(1 for word in formal_indicators if word in all_text)
        casual_count = sum(1 for word in casual_indicators if word in all_text)

        if formal_count > casual_count:
            return "formal"
        elif casual_count > formal_count:
            return "casual"
        return "mixed"


class DynamicDataGenerator:
    """Generates realistic, context-aware data for any form type."""

    # International names
    # Pakistani Male Names
    FIRST_NAMES_MALE = [
        "Muhammad", "Ali", "Ahmed", "Hassan", "Usman", "Bilal", "Omar", "Farhan",
        "Saad", "Hamza", "Imran", "Shahid", "Tariq", "Kashif", "Naveed", "Salman",
        "Faisal", "Waqas", "Asad", "Saeed", "Ibrahim", "Ismail", "Yousuf", "Yasir",
        "Waseem", "Kamran", "Shoaib", "Junaid", "Zubair", "Faizan", "Danish", "Haris",
        "Arslan", "Talha", "Rayyan", "Zayan", "Hammad", "Awais", "Bilawal", "Fahad",
        "Shahzaib", "Hashim", "Umair", "Waheed", "Tahir", "Noman", "Rizwan", "Atif"
    ]

    # Pakistani Female Names
    FIRST_NAMES_FEMALE = [
        "Fatima", "Ayesha", "Zainab", "Maryam", "Amina", "Sana", "Hira", "Sadia",
        "Rabia", "Khadija", "Nadia", "Shehnaz", "Nasreen", "Saima", "Rubina", "Asma",
        "Zahra", "Hania", "Alina", "Mahnoor", "Anaya", "Inaya", "Sara", "Malaika",
        "Arooj", "Laiba", "Alisha", "Hafsa", "Kainat", "Aleena", "Rida", "Aiza",
        "Kinza", "Mishal", "Zunaira", "Eshal", "Ayat", "Hoorain", "Wajiha", "Fiza",
        "Samina", "Naila", "Shazia", "Nusrat", "Farah", "Shumaila", "Nargis", "Yasmeen"
    ]

    # Pakistani Last Names
    LAST_NAMES = [
        "Khan", "Ahmed", "Siddiqui", "Sheikh", "Malik", "Butt", "Rana", "Javed",
        "Mirza", "Baig", "Hashmi", "Qureshi", "Ansari", "Farooqi", "Ismail", "Rizvi",
        "Naqvi", "Zafar", "Iqbal", "Shah", "Syed", "Hussain", "Abbasi", "Chaudhry",
        "Awan", "Lodhi", "Niazi", "Khattak", "Durrani", "Afridi", "Kakar", "Mengal",
        "Balooch", "Bhutto", "Gillani", "Soomro", "Junejo", "Mazari", "Leghari", "Khuhro",
        "Jatoi", "Shaikh", "Kazmi", "Jafri", "Rizvi", "Zaidi", "Gardezi", "Sial"
    ]

    # Pakistani Cities
    CITIES = [
        "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan",
        "Peshawar", "Quetta", "Hyderabad", "Sialkot", "Gujranwala", "Bahawalpur",
        "Sargodha", "Sukkur", "Larkana", "Sheikhupura", "Rahim Yar Khan", "Jhang",
        "Gujrat", "Mardan", "Kasur", "Mingora", "Dera Ghazi Khan", "Sahiwal",
        "Nawabshah", "Okara", "Mirpur Khas", "Chiniot", "Shikarpur", "Muzaffargarh",
        "Hafizabad", "Kohat", "Jacobabad", "Mandi Bahauddin", "Turbat", "Dadu", "Kambar"
    ]

    # Countries - primarily Pakistan with some neighboring countries
    COUNTRIES = [
        "Pakistan", "India", "Bangladesh", "Afghanistan", "Iran", "China", "Saudi Arabia",
        "UAE", "Qatar", "Kuwait", "Oman", "Bahrain", "Malaysia", "Turkey", "Indonesia",
        "United Kingdom", "United States", "Canada", "Australia", "Germany"
    ]

    # Countries
    COUNTRIES = [
        "United States", "United Kingdom", "Canada", "Australia", "Germany", "France",
        "Japan", "India", "Pakistan", "China", "Brazil", "Mexico", "Spain", "Italy",
        "Netherlands", "Sweden", "Norway", "Denmark", "Finland", "Poland", "UAE",
        "Saudi Arabia", "Singapore", "Thailand", "Malaysia", "Indonesia", "Philippines",
        "South Korea", "South Africa", "Nigeria", "Egypt", "Kenya", "Morocco"
    ]

    # Email domains - only Gmail (most popular in Pakistan)
    EMAIL_DOMAINS = [
        "gmail.com"
    ]

    # Pakistani Mobile Network Prefixes
    PHONE_PREFIXES = {
        "PK": [
            "+92 300", "+92 301", "+92 302", "+92 303", "+92 304", "+92 305", "+92 306", "+92 307", "+92 308", "+92 309",
            "+92 310", "+92 311", "+92 312", "+92 313", "+92 314", "+92 315", "+92 316", "+92 317", "+92 318", "+92 319",
            "+92 320", "+92 321", "+92 322", "+92 323", "+92 324", "+92 325", "+92 326", "+92 327", "+92 328", "+92 329",
            "+92 330", "+92 331", "+92 332", "+92 333", "+92 334", "+92 335", "+92 336", "+92 337", "+92 338", "+92 339",
            "+92 340", "+92 341", "+92 342", "+92 343", "+92 344", "+92 345", "+92 346", "+92 347", "+92 348", "+92 349"
        ],
        "DEFAULT": ["+92 300", "+92 301", "+92 302", "+92 321", "+92 322", "+92 323", "+92 330", "+92 331", "+92 332", "+92 333"]
    }

    # Departments by context
    DEPARTMENTS = {
        FormContext.MEDICAL: [
            "Cardiology", "Dermatology", "Emergency Medicine", "Family Medicine",
            "Gastroenterology", "General Surgery", "Internal Medicine", "Neurology",
            "Obstetrics and Gynecology", "Oncology", "Ophthalmology", "Orthopedics",
            "Pediatrics", "Psychiatry", "Radiology", "Urology", "Anesthesiology",
            "Pathology", "Pharmacy", "Nursing"
        ],
        FormContext.IT_TECH: [
            "Software Development", "Web Development", "Data Science", "Machine Learning",
            "DevOps", "Cybersecurity", "Network Administration", "Database Administration",
            "IT Support", "Quality Assurance", "UI/UX Design", "Product Management",
            "Cloud Computing", "Artificial Intelligence", "Mobile Development", "Backend",
            "Frontend", "Full Stack", "Systems Administration", "Technical Support"
        ],
        FormContext.EDUCATION: [
            "Mathematics", "Science", "English", "History", "Geography", "Physics",
            "Chemistry", "Biology", "Computer Science", "Art", "Music", "Physical Education",
            "Languages", "Literature", "Economics", "Psychology", "Sociology", "Philosophy",
            "Political Science", "Engineering"
        ],
        FormContext.BUSINESS: [
            "Marketing", "Sales", "Human Resources", "Finance", "Accounting",
            "Operations", "Customer Service", "Business Development",
            "Supply Chain", "Procurement", "Legal", "Administration",
            "Strategic Planning", "Public Relations", "Communications", "Research",
            "Training", "Facilities Management", "IT", "Executive"
        ],
        FormContext.EVENT: [
            "Event Planning", "Catering", "Entertainment", "Logistics", "Marketing",
            "Registration", "Security", "Audiovisual", "Decoration", "Transportation",
            "Hospitality", "Guest Services", "Sponsorship", "Media Relations"
        ],
        FormContext.GENERAL: [
            "General", "Administration", "Operations", "Management", "Support",
            "Services", "Coordination", "Planning", "Development", "Research"
        ]
    }

    # Job titles by context
    JOB_TITLES = {
        FormContext.MEDICAL: [
            "Registered Nurse", "Physician", "Surgeon", "Medical Assistant",
            "Pharmacist", "Radiologist", "Lab Technician", "Therapist",
            "Medical Director", "Chief of Medicine", "Resident", "Intern",
            "Nurse Practitioner", "Clinical Specialist", "Healthcare Administrator"
        ],
        FormContext.IT_TECH: [
            "Software Engineer", "Senior Developer", "Junior Developer", "DevOps Engineer",
            "Data Scientist", "Product Manager", "UI/UX Designer", "QA Engineer",
            "Systems Administrator", "Network Engineer", "Cloud Architect",
            "Technical Lead", "CTO", "IT Manager", "Support Specialist"
        ],
        FormContext.EDUCATION: [
            "Teacher", "Professor", "Teaching Assistant", "Principal", "Dean",
            "Department Head", "Lecturer", "Instructor", "Tutor", "Curriculum Developer",
            "Academic Advisor", "School Counselor", "Librarian", "Researcher"
        ],
        FormContext.BUSINESS: [
            "Manager", "Director", "Coordinator", "Analyst", "Specialist",
            "Supervisor", "Team Lead", "Consultant", "Executive", "VP",
            "Administrative Assistant", "Clerk", "Representative", "Associate"
        ],
        FormContext.GENERAL: [
            "Coordinator", "Specialist", "Manager", "Assistant", "Associate",
            "Representative", "Analyst", "Consultant", "Officer", "Administrator"
        ]
    }

    # Satisfaction levels
    SATISFACTION = [
        "Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied",
        "Excellent", "Good", "Average", "Poor", "Terrible"
    ]

    # Agreement levels
    AGREEMENT = [
        "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"
    ]

    # Yes/No
    YES_NO = ["Yes", "No"]

    # Education levels
    EDUCATION_LEVELS = [
        "High School", "Associate's Degree", "Bachelor's Degree", "Master's Degree",
        "PhD", "Diploma", "Certificate", "Some College", "Trade School", "Professional"
    ]

    # Experience levels
    EXPERIENCE_LEVELS = [
        "Less than 1 year", "1-2 years", "3-5 years", "5-10 years", "More than 10 years"
    ]

    @classmethod
    def generate_persona(cls, profile: FormProfile, submission_id: int = 0) -> Persona:
        """Generate a consistent persona for a single submission."""
        # Generate gender first
        gender = random.choice(["male", "female"])

        # Generate name
        if gender == "male":
            first = random.choice(cls.FIRST_NAMES_MALE)
        else:
            first = random.choice(cls.FIRST_NAMES_FEMALE)
        last = random.choice(cls.LAST_NAMES)
        name = f"{first} {last}"

        # Generate email based on name
        name_part = name.lower().replace(" ", ".")
        # Add some variation to email
        email_variations = [
            f"{name_part}@gmail.com",
            f"{name_part}{random.randint(1, 999)}@gmail.com",
            f"{name_part}{random.choice(['123', '786', '2024', '2025', '2026'])}@{random.choice(cls.EMAIL_DOMAINS)}",
            f"{first.lower()}.{last.lower()}{random.randint(1, 99)}@{random.choice(cls.EMAIL_DOMAINS)}"
        ]
        email = random.choice(email_variations)

        # Generate other consistent data
        age = cls.generate_age()
        phone = cls.generate_phone()
        address = cls.generate_address()
        city = random.choice(cls.CITIES)
        country = random.choice(cls.COUNTRIES)

        if gender == "male":
            gender_display = "Male"
        elif gender == "female":
            gender_display = "Female"
        else:
            gender_display = "Other"

        # Generate professional info based on context
        department = random.choice(cls.DEPARTMENTS.get(profile.context, cls.DEPARTMENTS[FormContext.GENERAL]))
        job_title = random.choice(cls.JOB_TITLES.get(profile.context, cls.JOB_TITLES[FormContext.GENERAL]))
        company = cls._generate_company_name(profile)
        education = random.choice(cls.EDUCATION_LEVELS)
        experience = random.choice(cls.EXPERIENCE_LEVELS)

        return Persona(
            name=name,
            first_name=first,
            last_name=last,
            email=email,
            phone=phone,
            address=address,
            city=city,
            country=country,
            age=age,
            gender=gender_display,
            company=company,
            job_title=job_title,
            department=department,
            education=education,
            experience=experience
        )

    @classmethod
    def generate_name(cls, gender: Optional[str] = None) -> str:
        """Generate a random name."""
        if gender is None:
            gender = random.choice(["male", "female"])

        if gender == "male":
            first = random.choice(cls.FIRST_NAMES_MALE)
        else:
            first = random.choice(cls.FIRST_NAMES_FEMALE)

        last = random.choice(cls.LAST_NAMES)
        return f"{first} {last}"

    @classmethod
    def generate_phone(cls, region: str = "PK") -> str:
        """Generate a random Pakistani phone number."""
        prefixes = cls.PHONE_PREFIXES.get(region, cls.PHONE_PREFIXES["PK"])
        prefix = random.choice(prefixes)
        number = "".join(random.choices("0123456789", k=7))
        return f"{prefix} {number[:3]} {number[3:]}"

    @classmethod
    def generate_email(cls, name: str) -> str:
        """Generate email from name using gmail.com only."""
        name_part = name.lower().replace(" ", ".")
        # Add some variation to avoid duplicates
        variations = [
            f"{name_part}@gmail.com",
            f"{name_part}{random.randint(1, 999)}@gmail.com",
            f"{name_part}{random.choice(['123', '786', '2024', '2025', '2026'])}@gmail.com"
        ]
        return random.choice(variations)

    @classmethod
    def generate_address(cls) -> str:
        """Generate a random address."""
        house = random.randint(1, 999)
        street_names = ["Main", "Oak", "Maple", "Pine", "Cedar", "Elm", "Washington",
                        "Lake", "Hill", "River", "Park", "Spring", "Valley", "Meadow"]
        street_types = ["Street", "Avenue", "Road", "Boulevard", "Lane", "Drive", "Way"]
        street = f"{random.choice(street_names)} {random.choice(street_types)}"
        city = random.choice(cls.CITIES)
        return f"{house} {street}, {city}"

    @classmethod
    def generate_age(cls, min_age: int = 18, max_age: int = 65) -> int:
        """Generate random age."""
        return random.randint(min_age, max_age)

    @classmethod
    def generate_date(cls, start_year: int = 2000, end_year: int = 2026) -> str:
        """Generate random date."""
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"

    @classmethod
    def generate_contextual_value(
        cls,
        label: str,
        field_type: str,
        profile: FormProfile,
        submission_id: int = 0,
        persona: Optional[Persona] = None
    ) -> Any:
        """Generate context-aware value based on field label and form profile.
        If persona is provided, use its consistent data for related fields.
        """
        if not label or label == "Unknown Field":
            if field_type == "text":
                return cls._generate_subjective_response(profile)
            return ""

        label_lower = label.lower()

        # Name fields - use persona if available
        if any(word in label_lower for word in ["name", "full name", "your name"]):
            if persona and persona.name:
                return persona.name
            return cls.generate_name()
        if "first name" in label_lower:
            if persona and persona.first_name:
                return persona.first_name
            name = cls.generate_name()
            return name.split()[0]
        if "last name" in label_lower or "surname" in label_lower:
            if persona and persona.last_name:
                return persona.last_name
            name = cls.generate_name()
            return name.split()[-1]

        # Contact fields - use persona if available
        if any(word in label_lower for word in ["phone", "mobile", "contact", "cell", "whatsapp"]):
            if persona and persona.phone:
                return persona.phone
            return cls.generate_phone()
        if any(word in label_lower for word in ["email", "e-mail", "mail"]):
            if persona and persona.email:
                return persona.email
            name = cls.generate_name()
            return cls.generate_email(name)

        # Location fields - use persona if available
        if any(word in label_lower for word in ["address", "location", "residence"]):
            if persona and persona.address:
                return persona.address
            return cls.generate_address()
        if any(word in label_lower for word in ["city", "town"]):
            if persona and persona.city:
                return persona.city
            return random.choice(cls.CITIES)
        if "country" in label_lower:
            if persona and persona.country:
                return persona.country
            return random.choice(cls.COUNTRIES)
        if "zip" in label_lower or "postal" in label_lower:
            return str(random.randint(10000, 99999))

        # Personal info - use persona if available
        if "age" in label_lower:
            if persona and persona.age:
                return str(persona.age)
            return str(cls.generate_age())
        if any(word in label_lower for word in ["gender", "sex"]):
            if persona and persona.gender:
                return persona.gender
            return random.choice(["Male", "Female", "Other"])
        if "date" in label_lower or "dob" in label_lower or "birth" in label_lower:
            return cls.generate_date()
        if "education" in label_lower or "qualification" in label_lower:
            if persona and persona.education:
                return persona.education
            return random.choice(cls.EDUCATION_LEVELS)

        # Professional fields - use persona if available
        if any(word in label_lower for word in ["department", "dept", "which department"]):
            if persona and persona.department:
                return persona.department
            return random.choice(cls.DEPARTMENTS.get(profile.context, cls.DEPARTMENTS[FormContext.GENERAL]))
        if any(word in label_lower for word in ["job title", "position", "role", "designation"]):
            if persona and persona.job_title:
                return persona.job_title
            return random.choice(cls.JOB_TITLES.get(profile.context, cls.JOB_TITLES[FormContext.GENERAL]))
        if "experience" in label_lower or "years of" in label_lower:
            if persona and persona.experience:
                return persona.experience
            return random.choice(cls.EXPERIENCE_LEVELS)
        if "company" in label_lower or "organization" in label_lower:
            if persona and persona.company:
                return persona.company
            return cls._generate_company_name(profile)

        # Rating/feedback fields
        if any(word in label_lower for word in ["satisfaction", "rating", "rate", "happy", "score"]):
            return random.choice(cls.SATISFACTION)
        if any(word in label_lower for word in ["agree", "opinion", "disagree"]):
            return random.choice(cls.AGREEMENT)
        if "yes" in label_lower or "no" in label_lower or "do you" in label_lower:
            return random.choice(cls.YES_NO)

        # Text/comment fields
        if any(word in label_lower for word in ["comment", "feedback", "suggestion", "review", "message", "tell us"]):
            return cls._generate_subjective_response(profile)

        # Number fields
        if "number" in label_lower or "quantity" in label_lower or "how many" in label_lower:
            return str(random.randint(1, 100))

        # Default based on field type
        if field_type == "text":
            return cls._generate_subjective_response(profile)

        return ""

    @classmethod
    def _generate_subjective_response(cls, profile: FormProfile) -> str:
        """Generate context-aware subjective response."""
        responses = {
            FormContext.MEDICAL: [
                "The healthcare service was excellent and the staff was very professional.",
                "I received great care and attention from the medical team.",
                "The facilities were clean and well-maintained.",
                "Wait times were reasonable and the process was smooth.",
                "The doctor was knowledgeable and took time to explain everything."
            ],
            FormContext.IT_TECH: [
                "The software solution works great and meets our requirements.",
                "The technical support team was very helpful and responsive.",
                "The system is user-friendly and intuitive to use.",
                "We've seen significant improvement in productivity since implementation.",
                "The code quality is excellent and well-documented."
            ],
            FormContext.EDUCATION: [
                "The course material was comprehensive and well-structured.",
                "The instructor was engaging and explained concepts clearly.",
                "I learned a lot from this class and would recommend it to others.",
                "The assignments were challenging but helped reinforce the concepts.",
                "The learning environment was supportive and encouraging."
            ],
            FormContext.BUSINESS: [
                "The business process improvements have increased our efficiency.",
                "The team collaboration has been excellent throughout the project.",
                "We've seen positive results since implementing the new strategy.",
                "The meeting was productive and action items were clear.",
                "The financial projections look promising for the next quarter."
            ],
            FormContext.EVENT: [
                "The event was well-organized and enjoyable.",
                "Great venue and excellent catering service.",
                "The speakers were informative and engaging.",
                "I had a wonderful time and met many interesting people.",
                "Everything ran smoothly and on schedule."
            ],
            FormContext.SURVEY: [
                "I found the questions clear and easy to understand.",
                "The survey covers all the important aspects.",
                "Happy to provide feedback to help with improvements.",
                "The experience was positive overall.",
                "Would be happy to participate in similar surveys in the future."
            ],
            FormContext.GENERAL: [
                "Overall a positive experience.",
                "Everything was handled professionally.",
                "I appreciate the opportunity to provide feedback.",
                "The process was straightforward and efficient.",
                "Thank you for considering my input."
            ]
        }

        context_responses = responses.get(profile.context, responses[FormContext.GENERAL])
        return random.choice(context_responses)

    @classmethod
    def _generate_company_name(cls, profile: FormProfile) -> str:
        """Generate a realistic company name based on context."""
        prefixes = ["Global", "Advanced", "Premier", "Elite", "Innovative", "Dynamic", "Strategic", "United"]
        suffixes = {
            FormContext.MEDICAL: ["Health", "Medical", "Care", "Wellness", "Clinics", "Healthcare"],
            FormContext.IT_TECH: ["Tech", "Solutions", "Systems", "Software", "Digital", "Innovations"],
            FormContext.EDUCATION: ["Academy", "Institute", "Learning", "Education", "School", "University"],
            FormContext.BUSINESS: ["Enterprises", "Group", "Corp", "Industries", "Associates", "Partners"],
            FormContext.GENERAL: ["Company", "Organization", "Services", "International", "Global"]
        }

        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes.get(profile.context, suffixes[FormContext.GENERAL]))
        return f"{prefix} {suffix}"

    @classmethod
    def generate_submission_data(
        cls,
        profile: FormProfile,
        fields: list[dict],
        submission_id: int
    ) -> dict:
        """Generate complete submission data for all fields."""
        data = {}
        for field in fields:
            label = field.get("label", "")
            field_type = field.get("field_type", "text")
            value = cls.generate_contextual_value(label, field_type, profile, submission_id)
            data[label] = value
        return data

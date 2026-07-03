"""Seed data for the Prism Academy session calendar.

On first run, store.py copies this into a local data_store.json that the app
reads/writes. Delete data_store.json to reset back to this seed.
"""

# Pods (programs). `short` is the key stored on each session.
PODS = [
    {"short": "Foundation (DC)",   "name": "Residential Interior Design Program – Foundation (Design Consultant)", "color": "#4A6741"},
    {"short": "Advanced (Sr. DC)", "name": "Advanced Interior Design Management & Leadership Program (Sr. DC)",     "color": "#B98A2E"},
    {"short": "Dovetail",          "name": "Dovetail Program (DA to DC)",                                          "color": "#2F6B6B"},
    {"short": "Design Manager",    "name": "Design Manager Program",                                               "color": "#B65C3C"},
    {"short": "Entrepreneurship",  "name": "Interior Design Entrepreneurship: The Business Playbook",              "color": "#7C6A9C"},
    {"short": "Campus Capstone",   "name": "Campus Capstone Program for Designers",                                "color": "#55708A"},
]

ADMIN_EMAIL = "pavithra.s@homelane.com"

# Pod owner + content lead per pod (editable by the program admin).
POD_LEADS = {
    "Foundation (DC)":   {"owner": "sachin.n@homelane.com",   "lead": "anviti.bhartiya@homelane.com"},
    "Advanced (Sr. DC)": {"owner": "shilpee.p@homelane.com",  "lead": "anviti.bhartiya@homelane.com"},
    "Dovetail":          {"owner": "rubin.jones@homelane.com","lead": "bhumika.s@homelane.com"},
    "Design Manager":    {"owner": "meera.a@homelane.com",    "lead": "bhumika.s@homelane.com"},
    "Entrepreneurship":  {"owner": "shilpee.p@homelane.com",  "lead": ""},
    "Campus Capstone":   {"owner": "shilpee.p@homelane.com",  "lead": ""},
}

# Faculty -> internal/external (used to auto-tag the picker).
FACULTY = {
    "Mathen Thomas": "internal", "Venkatesh": "internal", "Tanuj Choudhry": "internal",
    "Yeshwanth Chetty": "internal", "Sahana J Kashyap": "internal", "Aishwarya Srinivasan": "internal",
    "Levi Lawrence": "internal", "Anviti Bhartiya": "internal", "Vysnavi Anandaraj": "internal",
    "Somesh Manoharan": "internal", "Vivek Das (Vik)": "internal", "Surojit Ghosh": "internal",
    "Sushma Gowda": "internal", "Padmaja Das": "internal", "Archana M": "internal", "Abishek R": "internal",
    "Meera A": "internal", "Rajeev": "internal", "PRISM Team": "internal", "Internal HL/DC": "internal",
    "Maansi": "external", "Sachin Shetty": "external", "CIBI": "external", "Rajiv": "external",
    "Sachin": "external", "Gagan": "external", "Abhishek Bij": "external", "Shilpa Singh": "external",
    "Rajiv Bhakat": "external", "Maansi G": "external", "Abhishek/Design head": "external",
    "Via Email / WhatsApp": "internal", "Share via email": "internal", "To be decided": "internal",
}

# Participants (email IDs) per pod -> invited on Google Calendar sync alongside owner + lead.
PARTICIPANTS = {
    "Design Manager": [], "Entrepreneurship": [], "Campus Capstone": [],
    "Foundation (DC)": [
        "diksha.sharma@homelane.com", "pradeep.g@homelane.com", "swarnnim.jaiswal@homelane.com",
        "subhankar.saha@homelane.com", "pradipta.paul@homelane.com", "shruti.su@homelane.com",
        "ayasha.d@homelane.com", "aanchal.haveliker@homelane.com", "sanjay.peters@homelane.com",
        "tejaswini.pawar@homelane.com", "kavya.m@homelane.com", "simran.agarwal@homelane.com",
        "vrushali.chavan@homelane.com", "deekonda.lakhmi@homelane.com", "shreya.rajesh@homelane.com",
        "swarnika.b@homelane.com", "sandhya.ravichandran@homelane.com", "mariyam.asif@homelane.com",
        "tanushree.gupta@homelane.com", "archana.dubey@homelane.com", "tanya.singh@homelane.com",
        "dhruv.gajjar@homelane.com", "himashree.nath@homelane.com", "syed.esfar@homelane.com",
        "mythili.akanksha@homelane.com", "rahul.krishnan@homelane.com", "devshree.g@homelane.com",
        "vishnupriya.a@homelane.com", "choragudi.khyathi@designcafe.com", "jaicy.valliara@designcafe.com",
        "purnima.gupta@designcafe.com", "prashika.phillips@designcafe.com", "khushi.agarwal1@designcafe.com",
        "powlushi.dutta@designcafe.com", "pranjal.patil@designcafe.com", "kritika.shah@designcafe.com",
        "roshini.s@designcafe.com", "riya.panickar@designcafe.com", "sabita.bisht@designcafe.com",
        "ritika.singh@designcafe.com", "sahideena.afrin@designcafe.com", "indrani.das@designcafe.com",
        "sejal.shubhanand@homelane.com",
        "sayali.thakur@homelane.com", "pratheeka.k@homelane.com", "priti.sutar@homelane.com",
        "pratiksha.thorat@homelane.com", "kunali.gourigolla@homelane.com",
    ],
    "Dovetail": [
        "Poulomi.Banik@homelane.com", "Anchita.Nair@homelane.com", "Chandrika.Sah@homelane.com",
        "sheethal.shetty@homelane.com", "akshaya.santhanam@homelane.com", "vaibhav.s2@homelane.com",
        "dinesh.muthuraj@homelane.com", "mudassir.ahmed@homelane.com", "ajith.kumar@homelane.com",
        "veeresh.ts@homelane.com", "sarvesh.parab@homelane.com", "varalakshmi.r@homelane.com",
        "preethi.arulsamy@homelane.com", "yashasvi.kabra@homelane.com", "steffi.agarwal@homelane.com",
        "divyanshi.jain@homelane.com", "rupam.saxena@homelane.com", "vaibhavi.mahajan@homelane.com",
        "Aayushi.Singh@homelane.com", "dyawara.amulya@homelane.com", "vimalarasi.gv@homelane.com",
        "manisha.moni@homelane.com", "badruddeen.ismail@homelane.com", "Manvitha.Bondugula@homelane.com",
        "sanya.kapoor@homelane.com", "srushti.desai@homelane.com", "vishnu.paviraj@homelane.com",
        "nihal.choudhary@homelane.com", "priyanka.gawas@homelane.com", "shreya.jain@homelane.com",
        "tausif.md@homelane.com", "Rishipriya.j@homelane.com", "paramita.das@homelane.com",
        "Arpita.b2@homelane.com", "Srestha.Bhadra@homelane.com", "beejashree.thapa@homelane.com",
        "nidhi.takrani@homelane.com", "uchithra.raja@homelane.com", "divyashree.s@homelane.com",
        "vidhi.bahedia@homelane.com", "santhana.mari@homelane.com", "jayarani.n@homelane.com",
        "akash.s@homelane.com",
    ],
    "Advanced (Sr. DC)": [
        "aditya.chauhan@homelane.com", "manshi.sharma@homelane.com", "aditi.singh@homelane.com",
        "sanskruti.pagey@homelane.com", "vinita.l@homelane.com", "drishti.b2@homelane.com",
        "vishal.kumar@homelane.com", "tanushree.chaterjee@homelane.com", "ripon.chandra@homelane.com",
        "dilshad.anjum@homelane.com", "medha.bhattacharjee@homelane.com", "anusha.mullangi@homelane.com",
        "pratyasha.g@homelane.com", "suravi.b@homelane.com", "oeindrila.roy@homelane.com",
        "aashi.agarwal@homelane.com", "sushmitha.srinivasan@homelane.com", "selvakumar.joshiearnest@homelane.com",
        "ananya.upadhyay@homelane.com", "sonu.patel@homelane.com", "mahima.murjchandani@homelane.com",
        "sheetal.j@homelane.com", "chandni.s@homelane.com", "sandhya.narayanan@homelane.com",
        "irfan.m@homelane.com", "rabiya.b@homelane.com", "priyadharshini.i@homelane.com",
        "shanmathi.m@designcafe.com", "aditi.baazi@designcafe.com", "prachi.mahale@designcafe.com",
        "simran.agarwal@designcafe.com", "divyakshi.sarang@designcafe.com", "shubham.kalhapuream@designcafe.com",
        "vivek.rawat@designcafe.com", "viresh.chopra@designcafe.com", "akanksha.dhamnaskar@designcafe.com",
        "pooja.kumbharkar@designcafe.com", "shefali.tyagi@designcafe.com", "gourav.shrivastava@designcafe.com",
        "venkatesh.putcha@designcafe.com", "chinmayee.patra@designcafe.com", "hanny.srivastav@designcafe.com",
        "priyashi.panda@designcafe.com", "shaikh.subhan@designcafe.com", "faisul.rahman@designcafe.com",
    ],
}


def _s(pod, typ, title, fac, fkind, date, start, end, status, mode, loc="", note=""):
    return {"pod": pod, "type": typ, "title": title, "faculty": fac, "fkind": fkind,
            "date": date, "start": start, "end": end, "status": status, "mode": mode,
            "loc": loc, "note": note, "gcal_id": ""}


SESSIONS = [
    # ---- Dovetail (all virtual) ----
    _s("Dovetail", "module", "Leadership Induction", "Tanuj Choudhry", "internal", "2026-06-15", "11:00", "11:30", "confirmed", "virtual", "", "Day 1. Program objective, expectations, success definition."),
    _s("Dovetail", "module", "Process Overview", "Mathen Thomas", "internal", "2026-06-15", "12:30", "13:30", "confirmed", "virtual", "", "Lead to OB to Design to Production to Execution. Prep a presentation for the mock pitch."),
    _s("Dovetail", "module", "Lead & CRM Basics", "Yeshwanth Chetty", "internal", "2026-06-17", "11:30", "13:00", "confirmed", "virtual", "", "Day 2. Roster flow. Refresher + system demo."),
    _s("Dovetail", "module", "SC Pro Advanced", "To be confirmed", "internal", "2026-06-17", "13:30", "14:30", "proposed", "virtual", "", "SpaceCraft Pro UI, design wizard, Lookbook, Horizon, Photon. Faculty & time TBC."),
    _s("Dovetail", "module", "Designer Role & Performance", "Sahana J Kashyap", "internal", "2026-06-18", "11:30", "12:00", "confirmed", "virtual", "", "Day 3. Roles, career progression, incentives, performance management."),
    _s("Dovetail", "module", "Product Fundamentals", "Aishwarya Srinivasan", "internal", "2026-06-18", "12:00", "14:00", "confirmed", "virtual", "", "Intro to modular interiors, product catalogue."),
    _s("Dovetail", "module", "HDS 101", "Levi Lawrence", "internal", "2026-06-19", "11:30", "13:00", "confirmed", "virtual", "", "Day 4. Civil work, demolition, countertops, tiles; false ceiling & electrical."),
    _s("Dovetail", "assessment", "Assignment 1", "Anviti Bhartiya", "internal", "2026-06-20", "09:00", "18:00", "confirmed", "virtual", "", "Weekend. Custom to Persona Design + Categories, full 1st design output. Submit by Monday."),
    _s("Dovetail", "module", "HDS Drawings", "Vysnavi Anandaraj", "internal", "2026-06-22", "11:30", "13:00", "confirmed", "virtual", "", "Day 5. Traded goods along with 2Ds."),
    _s("Dovetail", "module", "RFQ along with Drawings", "Somesh Manoharan", "internal", "2026-06-22", "13:30", "14:30", "confirmed", "virtual", "", "New RFQ Tool quoting process. Custom workflow."),
    _s("Dovetail", "module", "Operational Design Validation", "Vivek Das (Vik)", "internal", "2026-06-24", "11:30", "13:00", "confirmed", "virtual", "", "Day 6. D1 visits, masking, design sign-off, D3 visits; ops collaboration."),
    _s("Dovetail", "module", "Execution Reality", "Surojit Ghosh", "internal", "2026-06-24", "13:30", "14:30", "confirmed", "virtual", "", "Real failures, ops challenges, design errors; production & delivery."),
    _s("Dovetail", "module", "Non-Standard Handling", "Sushma Gowda", "internal", "2026-06-25", "11:30", "13:00", "confirmed", "virtual", "", "Day 7. Avoidance, process, escalation."),
    _s("Dovetail", "module", "The Power of Consistency", "Maansi", "external", "2026-06-25", "13:30", "15:00", "confirmed", "virtual", "", ""),
    _s("Dovetail", "assessment", "Assignment 2", "To be confirmed", "internal", "2026-06-27", "09:00", "18:00", "proposed", "virtual", "", "Weekend. Custom + NSD to Persona Design + Categories, full output. Faculty TBC."),
    _s("Dovetail", "module", "Quote Optimization", "Padmaja Das", "internal", "2026-06-29", "11:30", "13:00", "confirmed", "virtual", "", "Day 8. Working to a budget & best design practices."),
    _s("Dovetail", "module", "Quality Check", "Archana M", "internal", "2026-06-29", "13:30", "14:30", "confirmed", "virtual", "", "Why QC is needed. QC process, rework handling."),
    _s("Dovetail", "module", "Quote 101", "Abishek R", "internal", "2026-07-01", "11:30", "12:30", "confirmed", "virtual", "", "Day 9. How to read and compare the quote."),
    _s("Dovetail", "module", "DCC / DA Support", "Meera A", "internal", "2026-07-01", "13:00", "13:30", "confirmed", "virtual", "", "DCC/DA workflow and what to expect."),
    _s("Dovetail", "module", "Designing for Lifestyles", "Rajeev", "internal", "2026-07-02", "11:30", "13:00", "confirmed", "virtual", "", "Day 10. Lifestyle decoding, empathy frameworks."),
    _s("Dovetail", "module", "The Art & Science of Customer Pitches", "Sachin Shetty", "external", "2026-07-03", "11:30", "13:00", "confirmed", "virtual", "", "Pitch diamond, storytelling for design presentations."),
    _s("Dovetail", "assessment", "Mock Pitch / DCC Evaluation", "Mock Pitch Panel", "internal", "2026-07-08", "11:30", "13:00", "proposed", "virtual", "", "Days 11-12 (Wed-Fri, date TBC). Panel: Shilpee, Rubin, Anviti, Foram, Padmaja, Meera."),
    # Practical exposure + certification placeholders (pod owner sets the real date)
    _s("Dovetail", "activity", "Shadow: On-ground Activities", "Design Manager (allocates)", "internal", "2026-06-16", "15:00", "17:00", "proposed", "virtual", "", "PLACEHOLDER. Throughout: Measurement Meeting, Masking, D2 sign-off & D3 visit."),
    _s("Dovetail", "activity", "Shadow: Design Discussions", "To be assigned", "internal", "2026-06-23", "14:00", "16:00", "proposed", "virtual", "", "PLACEHOLDER. 2 hrs. Observe real client meetings."),
    _s("Dovetail", "activity", "Shadow: Walkthrough Meetings", "To be assigned", "internal", "2026-06-26", "14:00", "16:00", "proposed", "virtual", "", "PLACEHOLDER. 2 hrs. Understand site execution realities."),
    _s("Dovetail", "activity", "Shadow: Closure Meetings", "To be assigned", "internal", "2026-06-30", "15:00", "16:00", "proposed", "virtual", "", "PLACEHOLDER. 1 hr. Observe sales closure dynamics."),
    _s("Dovetail", "activity", "Mock Walkthroughs with Managers", "To be assigned", "internal", "2026-07-06", "14:00", "16:00", "proposed", "virtual", "", "PLACEHOLDER. 2 hrs. Practice client communication."),
    _s("Dovetail", "activity", "HL Assessment Completion", "Self-paced", "internal", "2026-07-06", "10:00", "11:00", "proposed", "virtual", "", "PLACEHOLDER. Self-paced. Tool capability validation."),
    _s("Dovetail", "assessment", "Mock Client Pitch (Certification)", "To be assigned", "internal", "2026-07-09", "11:30", "12:30", "proposed", "virtual", "", "PLACEHOLDER. 1 hr. Evaluate presentation ability."),
    _s("Dovetail", "assessment", "DCC Evaluation (Certification)", "To be assigned", "internal", "2026-07-09", "14:00", "14:30", "proposed", "virtual", "", "PLACEHOLDER. 30 mins. Design Consultant readiness."),

    # ---- Advanced (Sr. DC) ----
    _s("Advanced (Sr. DC)", "module", "Orientation", "PRISM Team", "internal", "2026-06-08", "14:30", "15:30", "confirmed", "virtual", "", "Program kickoff: expectations, success definition."),
    _s("Advanced (Sr. DC)", "assessment", "Pre-Program Assessment", "PRISM Team", "internal", "2026-06-08", "10:00", "11:00", "proposed", "virtual", "", "1 hr. Time TBC."),
    _s("Advanced (Sr. DC)", "module", "Lab Day 1: Craft Leadership & Raising the Design Bar", "CIBI", "external", "2026-06-16", "10:00", "15:30", "confirmed", "inperson", "", "Lab Day 1. 5.5 hrs, in-person. Time TBC."),
    _s("Advanced (Sr. DC)", "module", "Lab Day 2: Customer Excellence through Leadership", "Rajiv", "external", "2026-06-17", "10:00", "15:30", "confirmed", "inperson", "", "Lab Day 2. 5.5 hrs, in-person. Time TBC."),
    _s("Advanced (Sr. DC)", "module", "Masterclass 1: Predictability at Scale", "Sachin", "external", "2026-07-02", "15:00", "17:00", "confirmed", "virtual", "", "4C: Contribution. 2 hrs."),
    _s("Advanced (Sr. DC)", "fireside", "Fireside Chat: Book / Artist / Leadership Talk", "To be decided", "internal", "2026-07-09", "11:00", "12:00", "proposed", "virtual", "", "1 hr. Faculty & time TBC."),
    _s("Advanced (Sr. DC)", "module", "Masterclass 2: Coaching for Design Success", "Maansi", "external", "2026-07-16", "11:00", "13:00", "confirmed", "virtual", "", "4C: Coaching. 2 hrs."),
    _s("Advanced (Sr. DC)", "module", "Masterclass 3: The Art & Science of Customer Pitches", "Gagan", "external", "2026-08-06", "11:00", "13:00", "confirmed", "virtual", "", "2 hrs."),
    _s("Advanced (Sr. DC)", "module", "Masterclass 4: The Strategic Shift", "Abhishek Bij", "external", "2026-08-12", "11:00", "13:00", "confirmed", "virtual", "", "4C: Customer. 2 hrs."),
    _s("Advanced (Sr. DC)", "assessment", "Challenge: Leadership Through Impact", "PRISM Team", "internal", "2026-08-13", "10:00", "11:00", "confirmed", "virtual", "", "Challenge shared via email. Time TBC."),
    _s("Advanced (Sr. DC)", "assessment", "Challenge Submission", "PRISM Team", "internal", "2026-09-04", "17:00", "18:00", "confirmed", "virtual", "", "Submission deadline (by end of day)."),
    _s("Advanced (Sr. DC)", "module", "Masterclass 5: Playing the Long Game", "Shilpa Singh", "external", "2026-09-02", "11:00", "13:00", "confirmed", "virtual", "", "4C: Career. 2 hrs."),
    _s("Advanced (Sr. DC)", "module", "Lab Day 3: From Strong Designers to Strong Systems", "Sachin", "external", "2026-09-15", "10:00", "15:30", "confirmed", "inperson", "", "Lab Day 3. 5.4 hrs, in-person. 4C: Craft + Contribution. Time TBC."),
    _s("Advanced (Sr. DC)", "module", "Lab Day 4: Culmination", "Internal HL/DC", "internal", "2026-09-16", "10:00", "14:00", "confirmed", "inperson", "", "Lab Day 4. 4 hrs, in-person. Time TBC."),
    _s("Advanced (Sr. DC)", "activity", "Post Read: Playbook", "PRISM Team", "internal", "2026-09-22", "10:00", "11:00", "proposed", "virtual", "", "Post-read playbook, self-paced. Placeholder time."),

    # ---- Foundation (DC) — PRISM Junior Cohort, Jun-Sep 2026 ----
    _s("Foundation (DC)", "module", "Orientation", "PRISM Team", "internal", "2026-06-12", "12:00", "13:00", "confirmed", "virtual", "", "Program kickoff. 1 hr."),
    _s("Foundation (DC)", "assessment", "Pre-Program Assessment", "Via Email / WhatsApp", "internal", "2026-06-12", "10:00", "11:00", "proposed", "virtual", "", "1 hr. Shared via email/WhatsApp. Time TBC."),
    _s("Foundation (DC)", "module", "Design Studio (Lab)", "Rajiv Bhakat", "external", "2026-06-15", "10:00", "16:00", "confirmed", "inperson", "", "Lab. 6 hrs, in-person. Time TBC."),
    _s("Foundation (DC)", "module", "Customer Experience Lab", "Rajiv Bhakat", "external", "2026-06-16", "09:00", "17:00", "confirmed", "inperson", "", "Lab. 8 hrs, in-person. Time TBC."),
    _s("Foundation (DC)", "module", "Masterclass 1: The Power of Consistency", "Maansi G", "external", "2026-07-02", "11:00", "13:00", "confirmed", "virtual", "", "2 hrs."),
    _s("Foundation (DC)", "fireside", "Fireside Chat: Book / Artist / Leadership Talk", "To be decided", "internal", "2026-07-09", "11:00", "12:00", "proposed", "virtual", "", "1 hr. Faculty & time TBC."),
    _s("Foundation (DC)", "module", "Masterclass 2: Bringing Lifestyles to Life", "Rajiv", "external", "2026-07-15", "11:00", "13:00", "confirmed", "virtual", "", "2 hrs."),
    _s("Foundation (DC)", "module", "Masterclass 3: The Art & Science of Customer Pitches", "Gagan", "external", "2026-08-06", "11:00", "13:00", "confirmed", "virtual", "", "2 hrs."),
    _s("Foundation (DC)", "module", "Masterclass 4: The Strategic Shift", "Abhishek/Design head", "external", "2026-08-12", "11:00", "13:00", "confirmed", "virtual", "", "2 hrs."),
    _s("Foundation (DC)", "assessment", "Design Challenge", "Share via email", "internal", "2026-08-19", "10:00", "11:00", "confirmed", "virtual", "", "Shared via email. Time TBC."),
    _s("Foundation (DC)", "assessment", "Breakthrough Project Submission", "PRISM Team", "internal", "2026-09-03", "17:00", "18:00", "confirmed", "virtual", "", "Submission deadline (by end of day)."),
    _s("Foundation (DC)", "module", "Lab: From Designers to Trusted Decision Partners", "Sachin", "external", "2026-09-08", "10:00", "14:30", "confirmed", "inperson", "", "Lab. 4.5 hrs, in-person. Time TBC."),
    _s("Foundation (DC)", "module", "Lab: PRISM Culmination Day", "Internal HL/DC", "internal", "2026-09-09", "10:00", "14:30", "confirmed", "inperson", "", "Lab. 4.5 hrs, in-person. Time TBC."),
    _s("Foundation (DC)", "activity", "Post Read: MC Takeaway Document", "PRISM Team", "internal", "2026-09-15", "10:00", "11:00", "proposed", "virtual", "", "Post-read takeaway document, self-paced."),
]

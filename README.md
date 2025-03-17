# Job Application Email Automation

This project automates the process of sending job application emails to multiple recruiters, handling email queueing and delivery efficiently.

## 🌐 Live Website
[https://testingproject.space](https://testingproject.space)  

- You can visit the website, enter your email, and receive a resume along with an introduction for a job application.  
- **Tired of sending the same email to recruiters over and over again? Here's the solution!**  
- Designed to save time and effort by automating the repetitive task of sending job applications to multiple recruiters.

---

## 🚀 How It Works
1. **Frontend**:
   - Built using HTML for user interface.
   - Simple form to input email and subject.

2. **Backend**:
   - Developed using **Node.js**.
   - Handles form submissions and inserts emails and subjects into a Redis queue.

3. **Queue Handling**:
   - Uses **Redis** to manage multiple email insertions and ensure they are processed in order.
   - Manages concurrent email processing using a queue-based system.

4. **Email Sending**:
   - A **Python script** processes the Redis queue and sends emails line-by-line to recruiters.
   - Handles subjects and content dynamically for each email.

---

## 🛠️ Technologies Used
- **Frontend**: HTML  
- **Backend**: Node.js  
- **Queue Management**: Redis  
- **Email Processing**: Python  

---


# LTCOE Campus — Professional Management Suite
## Faculty & Administrator Presentation Guide

This document outlines the core capabilities of the **LTCOE Campus** platform, structured to highlight technical sophistication and real-world utility during your presentation to the professor.

---

### 1. Unified Admission Intelligence
*   **Automated Lifecycle**: Manages the complete student journey from application to enrollment. 
*   **Decision Matrix**: Administrators can Approve, Reject, or Reset applications with a single click.
*   **Smart Roll-Generation**: Automatically assigns unique, branch-specific roll numbers (e.g., CE001, IT002) upon approval to ensure zero data collisions.
*   **Live Metrics**: The dashboard tracks "Pending Admissions" in real-time, ensuring no application is overlooked.

### 2. High-Fidelity Attendance Tracking
*   **Session Management**: Faculty can record attendance for specific subjects and academic years.
*   **Mass Marking Optimization**: "Mark All Present" and "Mark All Absent" shortcuts allow for rapid entry in large classrooms.
*   **Database Persistence**: Uses an optimized SQLite backend with `ON CONFLICT` logic to allow session corrections without duplicate entries.
*   **Real-time Synchronization**: Statistics (Present/Absent/Not Marked) and progress bars update instantly as data is toggled.

### 3. Advanced Analytics & Defaulter Tracking
*   **7-Day Trend Analysis**: A dynamic bar chart on the dashboard visualizes attendance patterns over the last week.
*   **Automatic Defaulter Detection**: The system identifies and flags students falling below the **75% mandatory threshold**.
*   **Branch-wise Performance**: Analyzes and compares attendance percentages across different departments (CE, IT, ENTC, etc.).
*   **Export Capabilities**: One-click **CSV Export** for generating official university records and offline audits.

### 4. Robust Role-Based Access Control (RBAC)
*   **Administrator**: Full system control including student deletion and global settings.
*   **Faculty**: Specialized access for managing admissions and recording classroom data.
*   **Student**: Secure, restricted "View-Only" profile. Students can track their own progress and history but are strictly prohibited from manipulating attendance or peer data.

### 5. Modern Technical Architecture
*   **Backend**: Flask (Python) REST API for high-performance data handling.
*   **Frontend**: A "Single Page Application" (SPA) design with vanilla JavaScript and CSS, ensuring a zero-lag, premium user experience.
*   **Database**: SQLite with relational integrity and foreign key constraints.

---

> [!TIP]
> **Key Talking Point for Professor**: 
> "The platform isn't just a digital register; it's a predictive tool. By identifying 'At-Risk' students automatically, it enables faculty to intervene early and improve overall academic outcomes."

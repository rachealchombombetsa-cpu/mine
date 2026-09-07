# test.pyimport os 
from datetime import datetime
import os
import os

def classify_session(duration):
    """Classify a study session based on duration."""
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"

def add_session(sessions):
    """Add a new study session to the list."""
    print("\n--- Add New Study Session ---")
    
    subject = input("Enter subject name: ").strip()
    if not subject:
        subject = "Unknown"
    
    topic = input("Enter topic covered: ").strip()
    if not topic:
        topic = "General"
    
    date_label = input("Enter date or day label (e.g., 2026-09-04 or Monday): ").strip()
    if not date_label:
        date_label = datetime.now().strftime("%Y-%m-%d")
    
    while True:
        try:
            duration = float(input("Enter duration in minutes: "))
            if duration > 0:
                break
            else:
                print("Duration must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    session = {
        "subject": subject,
        "topic": topic,
        "date": date_label,
        "duration": duration
    }
    
    sessions.append(session)
    print(f"✅ Session added successfully! ({classify_session(duration)})")

def view_sessions(sessions):
    """Display all logged sessions in a formatted table."""
    if not sessions:
        print("\n📋 No sessions logged yet.")
        return
    
    print("\n" + "="*80)
    print(f"{'📚 STUDY SESSIONS':^80}")
    print("="*80)
    print(f"{'#':<4} {'Subject':<20} {'Topic':<20} {'Date':<15} {'Duration':<10} {'Classification':<12}")
    print("-"*80)
    
    for idx, session in enumerate(sessions, 1):
        classification = classify_session(session["duration"])
        # Handle potential missing keys with safe access
        subject = session.get("subject", "Unknown")[:19]
        topic = session.get("topic", "General")[:19]
        date_label = session.get("date", "N/A")[:14]
        duration = session.get("duration", 0)
        
        print(f"{idx:<4} {subject:<20} {topic:<20} "
              f"{date_label:<15} {duration:<10.1f} {classification:<12}")
    
    print("="*80)
    total_minutes = sum(s.get("duration", 0) for s in sessions)
    total_hours = total_minutes / 60
    print(f"📊 Total sessions: {len(sessions)} | Total time: {total_hours:.2f} hours ({total_minutes:.1f} minutes)")

def search_by_subject(sessions):
    """Search and display sessions for a specific subject."""
    if not sessions:
        print("\n📋 No sessions logged yet.")
        return
    
    subject_search = input("\nEnter subject name to search: ").strip()
    if not subject_search:
        print("❌ Subject name cannot be empty.")
        return
    
    matching_sessions = []
    for s in sessions:
        if s.get("subject", "").lower() == subject_search.lower():
            matching_sessions.append(s)
    
    if not matching_sessions:
        print(f"\n❌ No sessions found for subject: '{subject_search}'")
        return
    
    # Get the actual subject name from first match
    actual_subject = matching_sessions[0].get("subject", subject_search)
    print(f"\n📚 Sessions for subject: '{actual_subject}'")
    print("-"*60)
    print(f"{'#':<4} {'Topic':<20} {'Date':<15} {'Duration':<10} {'Classification':<12}")
    print("-"*60)
    
    total_minutes = 0
    for idx, session in enumerate(matching_sessions, 1):
        classification = classify_session(session.get("duration", 0))
        topic = session.get("topic", "General")[:19]
        date_label = session.get("date", "N/A")[:14]
        duration = session.get("duration", 0)
        
        print(f"{idx:<4} {topic:<20} {date_label:<15} "
              f"{duration:<10.1f} {classification:<12}")
        total_minutes += duration
    
    total_hours = total_minutes / 60
    print("-"*60)
    print(f"📊 Total time spent on {actual_subject}: {total_hours:.2f} hours ({total_minutes:.1f} minutes)")

def study_statistics(sessions):
    """Display comprehensive study statistics."""
    if not sessions:
        print("\n📋 No sessions logged yet. Cannot compute statistics.")
        return
    
    print("\n" + "="*70)
    print(f"{'📊 STUDY STATISTICS':^70}")
    print("="*70)
    
    # Total hours overall
    total_minutes = sum(s.get("duration", 0) for s in sessions)
    total_hours = total_minutes / 60
    print(f"📈 Total study time: {total_hours:.2f} hours ({total_minutes:.1f} minutes)")
    
    # Per subject statistics
    subject_times = {}
    for session in sessions:
        subject = session.get("subject", "Unknown")
        duration = session.get("duration", 0)
        subject_times[subject] = subject_times.get(subject, 0) + duration
    
    print("\n📚 Study time per subject:")
    print("-"*50)
    for subject, minutes in sorted(subject_times.items(), key=lambda x: x[1], reverse=True):
        hours = minutes / 60
        print(f"  {subject}: {hours:.2f} hours ({minutes:.1f} minutes)")
    
    # Subject with least study time (weakest area)
    if subject_times:
        weakest_subject = min(subject_times, key=subject_times.get)
        weakest_time = subject_times[weakest_subject] / 60
        print(f"\n🔴 Weakest area (least studied): {weakest_subject} "
              f"({weakest_time:.2f} hours total)")
    
    # Single longest session
    if sessions:
        longest_session = max(sessions, key=lambda s: s.get("duration", 0))
        longest_duration = longest_session.get("duration", 0)
        longest_hours = longest_duration / 60
        subject = longest_session.get("subject", "Unknown")
        topic = longest_session.get("topic", "General")
        date_label = longest_session.get("date", "N/A")
        
        print(f"🏆 Longest single session: {subject} - "
              f"{topic} ({longest_hours:.2f} hours, "
              f"{longest_duration:.1f} minutes) on {date_label}")
    
    print("="*70)

def save_sessions(sessions, filename="study_log.txt"):
    """Save all sessions to a file."""
    try:
        with open(filename, 'w') as file:
            # Write header
            file.write("Subject,Topic,Date,Duration\n")
            # Write each session
            for session in sessions:
                subject = session.get("subject", "Unknown")
                topic = session.get("topic", "General")
                date_label = session.get("date", "N/A")
                duration = session.get("duration", 0)
                file.write(f"{subject},{topic},{date_label},{duration}\n")
        print(f"💾 Sessions saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving sessions: {e}")
        return False

def load_sessions(filename="study_log.txt"):
    """Load sessions from a file if it exists."""
    sessions = []
    
    if not os.path.exists(filename):
        return sessions  # File doesn't exist yet, return empty list
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                return sessions
            
            # Skip header if present
            start_idx = 1 if lines[0].strip().startswith("Subject") else 0
            
            for line in lines[start_idx:]:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(',')
                if len(parts) >= 4:
                    try:
                        session = {
                            "subject": parts[0].strip(),
                            "topic": parts[1].strip(),
                            "date": parts[2].strip(),
                            "duration": float(parts[3].strip())
                        }
                        sessions.append(session)
                    except ValueError:
                        # Skip invalid entries
                        continue
        
        print(f"📂 Loaded {len(sessions)} sessions from {filename}")
        return sessions
    except Exception as e:
        print(f"❌ Error loading sessions: {e}")
        return sessions

def main():
    """Main menu-driven interface."""
    sessions = load_sessions()
    
    while True:
        print("\n" + "="*50)
        print(f"{'📚 SMART STUDY PLANNER':^50}")
        print("="*50)
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        print("="*50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            add_session(sessions)
        elif choice == '2':
            view_sessions(sessions)
        elif choice == '3':
            search_by_subject(sessions)
        elif choice == '4':
            study_statistics(sessions)
        elif choice == '5':
            if save_sessions(sessions):
                print("👋 Goodbye! Happy studying!")
            else:
                print("⚠️  Sessions not saved. Exiting anyway.")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

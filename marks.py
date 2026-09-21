# 1. ఇన్‌పుట్ తీసుకోవడం
student_name = input("విద్యార్థి పేరు నమోదు చేయండి: ")
telugu = float(input("తెలుగు మార్కులు: "))
english = float(input("ఇంగ్లీష్ మార్కులు: "))
maths = float(input("మాథ్స్ మార్కులు: "))

# 2. గణన
total_marks = telugu + english + maths
percentage = (total_marks / 300) * 100

# 3. ఫెయిల్ అయిన సబ్జెక్టులు మరియు కౌంట్ ట్రాక్ చేసే వేరియబుల్స్
failed_subjects = []
fail_count = 0

# ఒక్కో సబ్జెక్ట్‌ను చెక్ చేయడం
if telugu < 35:
    failed_subjects.append("తెలుగు")
    fail_count += 1

if english < 35:
    failed_subjects.append("ఇంగ్లీష్")
    fail_count += 1

if maths < 35:
    failed_subjects.append("మాథ్స్")
    fail_count += 1

# 4. గ్రేడ్ మరియు ఫలితాలు ప్రింట్ చేయడం
print("\n" + "=" * 40)
print(f"విద్యార్థి పేరు: {student_name}")
print(f"మొత్తం మార్కులు: {total_marks} / 300")
print(f"శాతం (Percentage): {percentage:.2f}%")

# చెకింగ్ లాజిక్
if fail_count > 0:
    # లిస్ట్‌లోని సబ్జెక్టులను కామాలతో కలపడానికి ', '.join() వాడతాం
    subjects_str = ", ".join(failed_subjects)
    grade = f"F (ఫెయిల్ అయ్యారు - మొత్తం {fail_count} సబ్జెక్టులు: {subjects_str})"
elif percentage >= 90:
    grade = "A+ (చాలా బాగుంది!)"
elif percentage >= 75:
    grade = "A (బాగుంది)"
elif percentage >= 50:
    grade = "B (సగటు)"
else:
    grade = "C (పాస్)"

print(f"ఫలితం / గ్రేడ్: {grade}")
print("=" * 40)
# Really shitty script that prints out JSON of questions so it's a little easier to change. 
# Create JSON with the following command:
# python questions.py > questions.json
# Then convert that to a plist with the following command:
# plutil -convert xml1 questions.json -o Questions.plist

import json

questions = []
question_id = 0

range_texts_enum_hash = {
    'NOT AT ALL to EXTREMELY': 0,
    'NOT AT ALL to VERY STRONGLY': 1,
    'MOMENTARILY to VERY LONG TIME': 2,
    'VERY RESTED to VERY TIRED': 3,
    'NOT AT ALL to VERY MUCH SO': 4
    }

def range_num(s):
  return range_texts_enum_hash[s]

emotions = ['upset', 'angry', 'sad', 'depressed', 'nervous', 'anxious', 'happy', 'content', 'excited', 'energetic', 'relaxed', 'alert', 'stressed']
ruminations = [
    'it is hard for me to switch off my negative thoughts', 
    'it is hard for me to focus on something other than my negative thoughts',
    'I dwell on upsetting events'
    ]
self_compassions = [
    'I am kind to myself',
    'I am critical towards my flaws and weaknesses'
    ]
body_parts = ['Face', 'Head', 'Throat', 'Shoulder', 'Heart/chest', 'Stomach/digestion', 'Upper Back', 'Lower Back', 'Arms', 'Hands', 'Thigh', 'Knee', 'Feet/Ankle']
mindfulness_questions_negative = [
    'Right now, these negative sensations in my body bother me',
    'Right now, I try to push away these negative sensations',
    'Right now, I accept these negative sensations as they are',
    'I think these negative sensations in my body will last'
]
mindfulness_range_texts_negative = map(range_num, [
    'NOT AT ALL to EXTREMELY',
    'NOT AT ALL to VERY STRONGLY',
    'NOT AT ALL to VERY STRONGLY',
    'MOMENTARILY to VERY LONG TIME'
    ])

mindfulness_questions_positive = [
    'Right now, I enjoy these pleasant sensations in my body',
    'Right now, I try to prolong these pleasant sensations in my body',
    'I think these pleasant sensations in my body will last'
]
mindfulness_range_texts_positive = map(range_num, [
    'NOT AT ALL to EXTREMELY',
    'NOT AT ALL to VERY STRONGLY',
    'MOMENTARILY to VERY LONG TIME'
    ])
mindfulness_questions_emotion = [
    'I am lost in my emotions',
    'these emotions bother me',
    'I am lost in my thoughts',
    'these thoughts bother me'
]
mindfulness_range_texts_emotion = map(range_num, [
    'NOT AT ALL to EXTREMELY',
    'NOT AT ALL to VERY STRONGLY',
    'NOT AT ALL to EXTREMELY',
    'NOT AT ALL to VERY STRONGLY'
    ])

def create_question(text, type, category, other_dict={}):
  global question_id
  question = {
      "id": question_id,
      "text": text,
      "type": type,
      "category": category
      }
  question.update(other_dict)
  question_id += 1
  return question

def add_emotions():
  for emotion in emotions:
    text = "Right now I feel " + emotion.lower()
    type = "Emotion"
    category = "Emotions"
    others = {"emotion": emotion.title()}
    question = create_question(text, type, category, others)
    questions.append(question)

def add_ruminations():
  type = "Percent"
  category = "Ruminations"
  for rumination in ruminations:
    text = "Right now, " + rumination
    question = create_question(text, type, category)
    questions.append(question)

def add_self_compassions():
  type = "Percent"
  category = "Self-compassion"
  for message in self_compassions:
    text = "Right now, " + message
    question = create_question(text, type, category)
    questions.append(question)

def add_mindfulness_positive():
  type = "Multiselect"
  category = "Mindfulness"
  text = "Right now, I feel pleasant sensations in the following parts of my body"
  others = {"multi_select_options": body_parts}
  question = create_question(text, type, category, others)
  questions.append(question)
  
  type = "Percent"
  for message, range_text in zip(mindfulness_questions_positive, mindfulness_range_texts_positive):
    text = message
    others = {'range_text': range_text}
    question = create_question(text, type, category, others)
    questions.append(question)

def add_mindfulness_negative():
  type = "Multiselect"
  category = "Mindfulness"
  text = "Right now, I feel unpleasant sensations in the following parts of my body"
  others = {"multi_select_options": body_parts}
  question = create_question(text, type, category, others)
  questions.append(question)
  
  type = "Percent"
  for message, range_text in zip(mindfulness_questions_negative, mindfulness_range_texts_negative):
    text = message
    others = {'range_text': range_text}
    question = create_question(text, type, category, others)
    questions.append(question)

def add_mindfulness_emotions():
  category = "Mindfulness"
  type = "Percent"
  for message, range_text in zip(mindfulness_questions_emotion, mindfulness_range_texts_emotion):
    text = 'Right now, ' + message
    others = {'range_text': range_text}
    question = create_question(text, type, category, others)
    questions.append(question)

def add_life_satisfaction():
  category = "Life-satisfaction"
  type = "Percent"
  text = "Yesterday, I was satisfied with my life"
  questions.append(create_question(text, type, category))
    
def add_sleep():
  category = "Sleep"
  type = "Number"
  text = 'Tonight, I slept ... hours'
  questions.append(create_question(text, type, category, {'max': 16}))

  sleep_questions = [
    'Today, after my sleep, I felt', 
    'Tonight, I had bad dreams',
    'Tonight, I had good dreams'
    ]
  sleep_ranges = map(range_num, [
      'VERY RESTED to VERY TIRED',
      'NOT AT ALL to VERY MUCH SO',
      'NOT AT ALL to VERY MUCH SO'
      ])
  type = "Percent"
  for q, r in zip(sleep_questions, sleep_ranges):
    questions.append(create_question(q, type, category, {'range_text': r}))

def add_drinking():
  category = "Drinking"
  type = "Number"
  text = "Yesterday, I had ... alcoholic drinks"
  questions.append(create_question(text, type, category, {'max': 15}))

def add_smoking():
  category = "Smoking"
  type = "Number"
  text = "Yesterday, I had ... cigarettes"
  questions.append(create_question(text, type, category, {'max': 40}))

def add_physical():
  category = "Physical-activity"
  type = "Number"
  for q in ['walked', 'exercised', 'sat in front of a TV/video game/surfed the net']:
    text = 'Yesterday, I ' + q + ' ... minutes'
    questions.append(create_question(text, type, category, {'max': 300}))

def add_symptoms():
  category = "Symptoms"
  type = "Percent"
  range_text = 'NOT AT ALL to VERY MUCH SO'
  for q in ['Yesterday, I had pain', 'This pain bothered me']:
    questions.append(create_question(q, type, category, {"range_text": range_text}))

def add_management():
  category = "Stress-management"
  type = "Multiselect"
  text = "Yesterday, I used these techniques to deal with my stress"
  options = ['Took deep breaths', 'Checked in with my body', 'Took a moment to slow down', 'Paid deliberate attention to my actions']
  questions.append(create_question(text, type, category, {'multi_select_options': options}))

  text = "Yesterday, I tried to cheer myself up by"
  options = ['Socializing with my friends', 'Eating something delicious', 'Listening to music', 'Talking to people', 'Exercising or walking', 'Writing to friends']
  questions.append(create_question(text, type, category, {'multi_select_options': options}))

def main():
  global questions

  add_emotions()
  add_ruminations()
  add_self_compassions()
  add_mindfulness_positive()
  add_mindfulness_negative()
  add_mindfulness_emotions()

  momentary, questions = questions, []

  add_life_satisfaction()
  add_sleep()
  add_drinking()
  add_smoking()
  add_physical()
  add_symptoms()
  add_management()

  daily = questions

  questions = {'Momentary': momentary, 'Daily': daily}
  
  print json.dumps(questions, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
  main()


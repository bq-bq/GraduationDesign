class yijun_cal_obj1:
	def __init__(self):
		good = '''
			😀 Grinning Face
			😃 Grinning Face With Big Eyes
			😄 Grinning Face With Smiling Eyes
			😁 Beaming Face With Smiling Eyes
			😆 Grinning Squinting Face
			😅 Grinning Face With Sweat
			🤣 Rolling on the Floor Laughing
			😂 Face With Tears of Joy
			🙂 Slightly Smiling Face
			🙃 Upside-Down Face
			😉 Winking Face
			😊 Smiling Face With Smiling Eyes
			😇 Smiling Face With Halo
			😍 Smiling Face With Heart-Eyes
			🤩 Star-Struck
			😘 Face Blowing a Kiss
			😗 Kissing Face
			😚 Kissing Face With Closed Eyes
			😙 Kissing Face With Smiling Eyes
			😋 Face Savoring Food
			😛 Face With Tongue
			😜 Winking Face With Tongue
			🤪 Zany Face
			😝 Squinting Face With Tongue
			🤑 Money-Mouth Face
			🤗 Hugging Face
			🤠 Cowboy Hat Face
			😎 Smiling Face With Sunglasses
			🤓 Nerd Face
			😺 Grinning Cat
			😸 Grinning Cat With Smiling Eyes
			😻 Smiling Cat With Heart-Eyes
			😼 Cat With Wry Smile
			😽 Kissing Cat
			💋 Kiss Mark
			🖖 Vulcan Salute
			👌 OK Hand
			🤞 Crossed Fingers
			🤟 Love-You Gesture
			🤘 Sign of the Horns
			🤙 Call Me Hand
			👍 Thumbs Up
			✊ Raised Fist
			👏 Clapping Hands
			👐 Open Hands
			🤝 Handshake
			🙏 Folded Hands
			💪 Flexed Biceps
			🧠 Brain
			🙆 Person Gesturing OK
			🙆‍♂ Man Gesturing OK
			💐 Bouquet
			🌸 Cherry Blossom
			💮 White Flower
			🏵 Rosette
			🌹 Rose
			🥀 Wilted Flower
			🌺 Hibiscus
			🌻 Sunflower
			🌼 Blossom
			🌷 Tulip
			👶 Baby
			🧒 Child
			👦 Boy
			👧 Girl
			🧑 Person
			👱 Person: Blond Hair
			👨 Man
			🧔 Man: Beard
			👩 Woman
			🧓 Older Person
			👴 Old Man
			👵 Old Woman
			🙍 Person Frowning
			💝 Heart With Ribbon
			💖 Sparkling Heart
			💗 Growing Heart
			💓 Beating Heart
			💞 Revolving Hearts
			💕 Two Hearts
			💟 Heart Decoration
			💔 Broken Heart
			🧡 Orange Heart
			💛 Yellow Heart
			💚 Green Heart
			💙 Blue Heart
			💜 Purple Heart
			💯 Hundred Points
			'''

		bad = '''
			😔 Pensive Face
			😪 Sleepy Face
			🤤 Drooling Face
			😴 Sleeping Face
			😷 Face With Medical Mask
			🤒 Face With Thermometer
			🤕 Face With Head-Bandage
			🤢 Nauseated Face
			🤮 Face Vomiting
			🤧 Sneezing Face
			😵 Dizzy Face
			🤯 Exploding Head
			🧐 Face With Monocle
			😕 Confused Face
			😟 Worried Face
			🙁 Slightly Frowning Face
			😮 Face With Open Mouth
			😯 Hushed Face
			😲 Astonished Face
			😳 Flushed Face
			😦 Frowning Face With Open Mouth
			😧 Anguished Face
			😨 Fearful Face
			😰 Anxious Face With Sweat
			😥 Sad but Relieved Face
			😢 Crying Face
			😭 Loudly Crying Face
			😱 Face Screaming in Fear
			😖 Confounded Face
			😣 Persevering Face
			😞 Disappointed Face
			😓 Downcast Face With Sweat
			😩 Weary Face
			😫 Tired Face
			😤 Face With Steam From Nose
			😡 Pouting Face
			😠 Angry Face
			🤬 Face With Symbols on Mouth
			😈 Smiling Face With Horns
			👿 Angry Face With Horns
			💀 Skull
			💩 Pile of Poo
			🤡 Clown Face
			👹 Ogre
			👺 Goblin
			👻 Ghost
			👽 Alien
			👾 Alien Monster
			🤖 Robot
			😹 Cat With Tears of Joy
			🙀 Weary Cat
			😿 Crying Cat
			😾 Pouting Cat
			👎 Thumbs Down
			👊 Oncoming Fist
			🤛 Left-Facing Fist
			🤜 Right-Facing Fist
			👀 Eyes
			👁 Eye
			👅 Tongue
			👄 Mouth
			🙅 Person Gesturing No
			🤦 Person Facepalming
			🤦‍ Man Facepalming
			🤷 Person Shrugging
			🙈 See-No-Evil Monkey
			🙉 Hear-No-Evil Monkey
			🙊 Speak-No-Evil Monkey
			🐶 Dog Face
			🐷 Pig Face
			🐖 Pig
			🐗 Boar
			🐽 Pig Nose
			🐻 Bear
			🐨 Koala
			🐼 Panda
			🐔 Chicken
			🐓 Rooster
			🐣 Hatching Chick
			🐤 Baby Chick
			🐥 Front-Facing Baby Chick
			🐦 Bird
			🐧 Penguin
			⛈ Cloud With Lightning and Rain
			🌤 Sun Behind Small Cloud
			🌥 Sun Behind Large Cloud
			🌦 Sun Behind Rain Cloud
			🌧 Cloud With Rain
			🌨 Cloud With Snow
			🌩 Cloud With Lightning
			🌪 Tornado
			'''

		num = '''
			0️⃣ Keycap Digit Zero
			1️⃣ Keycap Digit One
			2️⃣ Keycap Digit Two
			3️⃣ Keycap Digit Three
			4️⃣ Keycap Digit Four
			5️⃣ Keycap Digit Five
			6️⃣ Keycap Digit Six
			7️⃣ Keycap Digit Seven
			8️⃣ Keycap Digit Eight
			9️⃣ Keycap Digit Nine
			🔟 Keycap: 10
			'''

		sign = '''
			➕ Plus Sign
			➖ Minus Sign
			❔ White Question Mark
			'''
		
		# ➕ ➖ ➗ ✖️

		good = [x.strip() for x in good.split('\n') if x.strip()]
		bad = [x.strip() for x in bad.split('\n') if x.strip()]
		num = [x.strip() for x in num.split('\n') if x.strip()]
		sign = [x.strip() for x in sign.split('\n') if x.strip()]
		
		text = html.SPAN()
		input = html.INPUT(style={'font-size':'30px'}, **{'size':2, 'type':'text'})
		button = html.BUTTON('OK', style={'margin':'15px'}, **{'type':'button', 'class':'btn btn-primary'})
		fig = html.DIV(style={'font-size':'150px'})
		
		self.elt = html.DIV(html.H1(text + input + button) + fig)

		def get_num(n):
			nonlocal num
			res = ''
			if n == 0:
				res += num[0][:3]
			else:
				d = []
				while n > 0:
					d.append(n % 10)
					n = n // 10
				for i in reversed(d):
					res += num[i][:3]
			return res

		next=0
		answer = None

		def randint(s, e):
			nonlocal next
			next = (next * 1103515245 + 12345) % 32768
			return next % (e-s) + s

		def change(ev):
			nonlocal input, answer
			input_text = input.value.strip()
			try:
				input_int = int(input_text)
			except:
				input_int = -1000
			print(input_int, answer)
			if input_int != answer:
				show_bad()
			else:
				show_good()
				next_problem()

		def show_bad():
			nonlocal fig, bad
			fig.text = bad[randint(0, len(bad)-1)][:2]

		def show_good():
			nonlocal fig, good
			fig.text = good[randint(0, len(good)-1)][:2]

		def next_problem():
			nonlocal answer, sign, text, input
			d1 = randint(0,100)
			d2 = randint(0,100)
			if d1 > d2:
				d1, d2 = d2, d1
			d0 = d2 - d1
			op = randint(0,2)
			if op == 0:
				res = get_num(d0) + sign[op][0] + get_num(d1) + ' = '
				answer = d2
			else:
				res = get_num(d2) + sign[op][0] + get_num(d1) + ' = '
				answer = d0
			text.text = res
			input.value = ''

		button.bind('click', change)
		next_problem()
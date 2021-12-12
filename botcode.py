from telegram.ext import *
from telegram import *
import praw,random,datetime,threading,time,psycopg2

#telegram
API_KEY = '#telegram bot api key'
bot = Bot(API_KEY)

#reddit
reddit = praw.Reddit(client_id='#reddit client id', \
                     client_secret='#reddit client secret', \
                     user_agent='#reddit user agent', \
                     username='#reddit user name', \
                     password='#reddit password')

#postgreSQL
connection = psycopg2.connect(host='#database host',
                        database='#database name',
                        port = '#database port',
                        user='#database user',
                        password='#database password')
cursor = connection.cursor()

ID = #chat id of your bot logger group

def news(update,context):
    #store
    cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(update.message.message_id),str(update.message.chat_id),str(update.message.date)))
    connection.commit()
    
    #send
    subreddit = reddit.subreddit('worldnews')
    msg = update.message.reply_text('3 hot news articles on worldnews:')
    #store
    cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
    connection.commit()
    #send
    for submission in subreddit.hot(limit = 3):
        msg = bot.sendMessage(chat_id = update.message.chat_id,text = submission.url)
        cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
        connection.commit()
    
def memes(update,context):
    #anger
    angrychance = random.randrange(1,301)
    if int(angrychance) ==100:
        msg = bot.sendMessage(chat_id = update.message.chat_id,text =""""fetch those links for us mememachine." Thats what they say to me, "bring me this photo mememachine." \
        "tell us a joke."Here I am, brain the size of a planet, and they ask me to read you a reddit post, call that job satisfaction, cause I dont. Go on, have your joke, now laugh.""")
        cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
        connection.commit()
    
    #store
    cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(update.message.message_id),str(update.message.chat_id),str(update.message.date)))
    connection.commit()
    
    sublist = {'dogs':['dogswithjobs','WhatsWrongWithYourDog','corgi','goldenretrievers','blop','PuppySmiles','woof_irl','rarepuppers','HappyWoofGifs']\
               ,'memes':['Memes_of_the_dank','fffffffuuuuuuuuuuuu','BikiniBottomTwitter','me_irl','memes','dankmemes','antimeme','shitposting','comedyheaven','wholesomememes','MemesIRL']\
               ,'cats':['Kitler','MEOW_IRL','cats','grumpycats','IllegallySmolCats','catsarealiens','Catloaf','Purrito','Blep','airplaneears']\
               ,'awwnimals':['Otters','Rabbits','ferrets','aww','AnimalsBeingDerps','Eyebleach','awwwtf','awwducational','foxes','RATS','stoppedworking','redpandas']\
               ,'blursedimages':['blursedimages'],'jokes':['jokes','dadjokes','unclejokes','cleanjokes']}
    #gets the message that user sent to use for subreddit
    words = str(update.message['text'])[1:].split('@')
    subreddit = reddit.subreddit(random.choice(sublist[words[0]]))
    posts = [post for post in subreddit.hot(limit=50)]
    random_post=posts[random.randint(0, 49)]
    
    if str(words[0]).lower() =="""jokes""":
        while random_post.stickied:
            random_post=posts[random.randint(0, 49)]
        msg = bot.sendMessage(chat_id = update.message.chat_id,text = random_post.title+'\n'+random_post.selftext+'\n(r/'+str(subreddit)+')')
        cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
        connection.commit()
    else:
        count = 0
        while (not random_post.url.endswith(tuple([".jpg",".png",".gif"])))or(random_post.stickied)or(random_post.over_18 == True) and (count<5):
            random_post=posts[random.randint(0, 49)]
            count+=1
        #send gifs and images
        hold = True
        count = 0
        while hold and (count<3):
            try:
                if (".gif" in random_post.url):
                    msg = bot.sendVideo(chat_id = update.message.chat_id,video = random_post.url,caption = random_post.title+' (r/'+str(subreddit)+')')
                    cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
                    connection.commit()
                else:
                    msg = bot.sendPhoto(chat_id = update.message.chat_id,photo = random_post.url,caption = random_post.title+' (r/'+str(subreddit)+')')
                    cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
                    connection.commit()
                hold = False
                
            except Exception as error:
                bot.sendMessage(chat_id = ID, text = 'error while sending:'+str(random_post.url)+'error: '+error)
                innerCount = 0
                random_post=posts[random.randint(0, 49)]
                while (not random_post.url.endswith(tuple([".jpg",".png",".gif"])))or(random_post.stickied)or(random_post.over_18 == True) and (innerCount>5):
                    random_post=posts[random.randint(0, 49)]
                    innerCount+=1
                    
                if count >=2:
                    msg = bot.sendMessage(chat_id = update.message.chat_id,text = str(random_post.url))
                    cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
                    connection.commit()
                count+=1
def translate(update,context):
    try:
        bettertext = str(update.message.reply_to_message.text).lower().replace('l','w')
        bettertext = bettertext.replace('r','w')
        bettertext = bettertext.replace('j','w')
        bot.sendMessage(chat_id = update.message.chat_id, text = bettertext)
        #when message is empty
    except AttributeError:
        if str(update.message.text).lower().strip() == '/translate':
            #store
            cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(update.message.message_id),str(update.message.chat_id),str(update.message.date)))
            connection.commit()
            msg = bot.sendMessage(chat_id = update.message.chat_id, text = 'I dont see any text, are you sure you have a functioning brain?')
            cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
            connection.commit()
            
        elif str(update.message.text).lower().strip()== '/translate@simpmachinebot':
            #store
            cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(update.message.message_id),str(update.message.chat_id),str(update.message.date)))
            connection.commit()
            msg = bot.sendMessage(chat_id = update.message.chat_id, text = 'I dont see any text, are you sure you have a functioning brain?')
            cursor.execute("""INSERT INTO messages (message_id,chat_id,date) VALUES (%s,%s,%s);""",(str(msg['message_id']),str(msg['chat']['id']),str(msg['date'])))
            connection.commit()

        else:
            bettertext = str(update.message.text).lower().replace('l','w')
            bettertext = bettertext.replace('r','w')
            bettertext = bettertext.replace('j','w')
            if bettertext.startswith('/twanswate '):
                bot.sendMessage(chat_id = update.message.chat_id, text = bettertext[10:])
            else:
                bot.sendMessage(chat_id = update.message.chat_id, text = bettertext[25:])

def help(update, context):
    update.message.reply_text('Type /translate while tagging some text to uwuify it, subreddits supported right now:\n /memes\n/desimemes\n/cats\n/awwnimals\n/blursedimages\n/news\n/jokes\n/dogs\n(I delete messages I send after 10 hours)')
    
def handle_message(update,context):
    #profanityList = ['stfu','shut up','bad bot']
    if 'stfu' in str(update.message['text']).lower():
        update.message.reply_text('no u')
    elif (str(update.message['text']).startswith('/'))and('@simpmachinebot' in str(update.message['text'])):
        bot.sendMessage(chat_id = update.message.chat_id,text ='It gives me a headache just trying to think down to your level.')
    
#deletor multithread
def deletor():
    bot.sendMessage(chat_id = ID, text = 'multithreading started....')
    while True:
        try:
            #grabs the first entry from database
            cursor.execute('SELECT * FROM messages ORDER BY date ASC LIMIT 1;')
            record = cursor.fetchone()
            #calculates elapsed time
            origin = datetime.datetime.strptime(record[2][:19],"%Y-%m-%d %H:%M:%S")
            today = datetime.datetime.now()
            elapsed = today - origin
            if elapsed.total_seconds() >= 36000:
                bot.deleteMessage(str(record[1]),int(record[0]))
                cursor.execute("""DELETE FROM messages WHERE message_id = %s AND chat_id = %s;""",(str(record[0]),str(record[1])))
                connection.commit()
                bot.sendMessage(chat_id = ID, text = 'Deleted '+str(record[0])+','+str(record[1])[::2])
                time.sleep(30)
            else:
                bot.sendMessage(chat_id = ID, text = str(int(elapsed.total_seconds())))
                time.sleep(300)
            #exception handling
        except TelegramError as e:
            bot.sendMessage(chat_id = ID, text = 'Telegram:- '+str(e))
            cursor.execute("""DELETE FROM messages WHERE message_id = %s AND chat_id = %s;""",(str(record[0]),str(record[1])))
            connection.commit()
            time.sleep(60)
        except Exception as error:
            if str(error)=="""'NoneType' object is not subscriptable""":
                bot.sendMessage(chat_id = ID, text = 'Empty.')
                time.sleep(600)
            else:
                bot.sendMessage(chat_id = ID, text = str(error))
                time.sleep(60)
            
def main():
    try:
        updater = Updater(API_KEY, use_context = True)
        dp = updater.dispatcher
        bot.sendMessage(chat_id = ID, text = 'Bot started...')
        
        dp.add_handler(CommandHandler("news",news))
        dp.add_handler(CommandHandler("jokes",memes))
        dp.add_handler(CommandHandler("memes",memes))
        dp.add_handler(CommandHandler("cats",memes))
        dp.add_handler(CommandHandler("awwnimals",memes))
        dp.add_handler(CommandHandler("blursedimages",memes))
        dp.add_handler(CommandHandler("dogs",memes))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("translate", translate))
        dp.add_handler(MessageHandler(Filters.text,handle_message))
        
        updater.start_polling()
        updater.idle()
    except Exception as error:
        bot.sendMessage(chat_id = ID, text = 'BOT ERROR:-'+str(error))
        
threadObj = threading.Thread(target = deletor)
threadObj.start()
main()

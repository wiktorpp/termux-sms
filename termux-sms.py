import subprocess

true = 1
false = 0

def _execute(func: str, stdin: str = ""):
    p = subprocess.Popen(
        func,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True
    )
    output, err = p.communicate(stdin)
    return output + err

messages = dict()

messages = {
    2: {
        "threadid": 28,
        "type": "inbox",
        "read": true,
        "number": "+48661255197",
        "received": "2022-12-16 11:34:47",
        "body": "test",
        "_id": 2
    }
}

def _get_messages_from_phone(limit=10, offset=0, type="all"):
    return eval(_execute(f"termux-sms-list -l {limit} -o {offset} -t {type}"))

def _add_new_message(message):
    message[message._id] = message

def get_new_messages(type="inbox"):
    messages_from_phone = _get_messages_from_phone()
    for message in messages_from_phone:
        if message["_id"] in messages.keys():
            print(f"{message['_id']} already in the list")
            pass
        else:
            print(f"{message['_id']} not in the list")
            messages[message["_id"]] = message
            if message["type"] == type:
                yield message
            if type == "all":
                yield message

def send_message(number: int, body: str):
    _execute(f"termux-sms-send -n {str(number)} {body}")
    #for _ in range(3):
    #    messages_from_phone = _get_messages_from_phone(limit=1, type="sent")
    x=_get_messages_from_phone(limit=1, type="sent")
    print(x)
    if len(x) == 0:
        return
    else:
        raise TimeoutError

send_message(123456, "test2")





print(list(get_new_messages(type="all")))

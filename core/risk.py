def calculate_risk(price):

    stop=price*0.995

    tp1=price*1.005

    tp2=price*1.01

    tp3=price*1.02

    return {

        "stop":stop,
        "tp1":tp1,
        "tp2":tp2,
        "tp3":tp3

    }

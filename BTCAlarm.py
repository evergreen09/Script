import ccxt
import time
import threading
from playsound import playsound

class BitcoinAlarmApp:
    def __init__(self):
        self.exchange = ccxt.binance()
        self.alarms = {"1": [], "0": []}
        self.alarm_playing = False

    def add_alarm(self):
        if len(self.alarms["1"]) + len(self.alarms["0"]) < 10:
            alarm_type = input("Enter type of alarm [Upward(1)/Downward(0)]: ")
            if alarm_type not in ["1", "0"]:
                print("Invalid alarm type. Please select either Upward(1) or Downward(0)")
                return
            price = float(input("Enter the price at which to set the alarm: "))
            self.alarms[alarm_type].append(price)
            print(f"{alarm_type.capitalize()} alarm set at {price}")
        else:
            print("You can only set upto 10 alarms")

    def check_price(self):
        current_price = self.exchange.fetch_ticker('BTC/USDT')['close']
        print(f"Current price: {current_price}")
        return current_price

    def alarm_off(self):
        while self.alarm_playing:
            if input() == 'off':
                self.alarm_playing = False

    def alarm_on(self):
        while self.alarm_playing:
            playsound('alarm.mp3')  # Replace with your own alarm sound file

    def run(self):
        current_price = self.check_price()
        for alarm in self.alarms["1"][:]:
            if current_price >= alarm:
                print(f"1 alarm! Price crossed {alarm}")
                self.alarm_playing = True
                alarm_thread = threading.Thread(target=self.alarm_on)
                alarm_off_thread = threading.Thread(target=self.alarm_off)
                alarm_thread.start()
                alarm_off_thread.start()
                self.alarms["1"].remove(alarm)
        for alarm in self.alarms["0"][:]:
            if current_price <= alarm:
                print(f"0 alarm! Price dropped below {alarm}")
                self.alarm_playing = True
                alarm_thread = threading.Thread(target=self.alarm_on)
                alarm_off_thread = threading.Thread(target=self.alarm_off)
                alarm_thread.start()
                alarm_off_thread.start()
                self.alarms["0"].remove(alarm)

    def start(self):
        while True:
            print("\n")
            print("Menu")
            print("1. Add alarm")
            print("2. Check prices")
            print("3. Exit")
            option = int(input("Select an option: "))
            if option == 1:
                self.add_alarm()
            elif option == 2:
                self.run()
            elif option == 3:
                break
            else:
                print("Invalid option. Please select again.")

app = BitcoinAlarmApp()
app.start()

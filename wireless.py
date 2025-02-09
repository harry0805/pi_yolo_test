from rpi_rf import RFDevice
import threading


class SignalControl:
    def __init__(self, rf_device: RFDevice, on_code: int=1234, off_code: int=5678, ping_interval: int|float=1):
        """
        Controls signal sending for ON and OFF signals. When ON, continuously sends the ON signal at a specified interval.

        Args:
            rf_device: An instance of the RFDevice with enabled tx
            on_code: ON signal code
            off_code: OFF signal code
            ping_interval: Time interval between ON signals
        """
        self.rf_device = rf_device
        self.on_code = int(on_code)
        self.off_code = int(off_code)
        self.ping_interval = ping_interval

        self._stopped = False
        self._state = False
        self._cond = threading.Condition()
        self._thread = threading.Thread(target=self._signal_thread, daemon=True)
        self._thread.start()

    def _signal_thread(self):
        while not self._stopped:
            # with self._cond:
            #     current_mode = self._mode

            if self._state:
                # Continuous send the ON signal
                self.rf_device.tx_code(self.on_code)
                # When the mode is still ON, wait for the ping interval
                if self._state:
                    with self._cond:
                        self._cond.wait(self.ping_interval)
            else:
                # Send the OFF signal one time
                self.rf_device.tx_code(self.off_code)
                if not self._state:
                    with self._cond:
                        self._cond.wait()
                # with self._cond:
                #     # Wait for mode change or stop signal
                #     while not self.stopped and not self._mode:
                #         self._cond.wait()

    def set_state(self, state):
        state = bool(state)
        with self._cond:
            # Only act when there is a change
            if self._state != state:
                self._state = state
                # Notify the thread that mode has changed.
                self._cond.notify_all()

    def stop(self):
        with self._cond:
            self._stopped = True
            self._cond.notify_all()
        self._thread.join()


if __name__ == "__main__":
    # <<<Testing with manual control>>>
    PIN = 17  # GPIO pin

    rfdevice = RFDevice(PIN)
    rfdevice.enable_tx()
    signal = SignalControl(rfdevice)

    while True:
        # Send OFF signal
        signal.set_state(False)
        print(">>> Sending OFF signal <<<")
        input()

        # Send ON signal
        signal.set_state(True)
        print(">>> Sending ON signal <<<")
        input()

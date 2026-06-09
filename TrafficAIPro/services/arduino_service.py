"""Optional Arduino traffic light integration."""

from __future__ import annotations

from typing import Any


class ArduinoService:
    """Send vehicle counts to an Arduino over serial, or simulate them in mock mode."""

    def __init__(
        self,
        port: str | None = None,
        baudrate: int = 9600,
        timeout: float = 1.0,
        mock_mode: bool = True,
    ) -> None:
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.mock_mode = mock_mode
        self._serial: Any | None = None
        self._fallback_to_mock = False
        self.last_sent_data = "None"
        self.last_level = "G"
        self.last_error = ""

    @property
    def is_connected(self) -> bool:
        return self._serial is not None and bool(getattr(self._serial, "is_open", False))

    @property
    def is_mock(self) -> bool:
        return self.mock_mode or self._fallback_to_mock or not self.is_connected

    @property
    def mode_label(self) -> str:
        return "Connected" if self.is_connected and not self._fallback_to_mock else "Mock"

    @property
    def traffic_light_label(self) -> str:
        return {"G": "Green", "Y": "Yellow", "R": "Red"}.get(self.last_level, "Green")

    def connect(self) -> bool:
        """Connect to Arduino serial, or keep the service in mock mode."""
        self._fallback_to_mock = False

        if self.mock_mode:
            print("[ArduinoService] Mock mode enabled. Serial connection skipped.")
            return True

        if not self.port:
            self.last_error = "COM port is missing. Falling back to mock mode."
            self._fallback_to_mock = True
            print(f"[ArduinoService] {self.last_error}")
            return False

        try:
            import serial
        except ImportError:
            self.last_error = "pyserial is not installed. Falling back to mock mode."
            self._fallback_to_mock = True
            print(f"[ArduinoService] {self.last_error}")
            return False

        try:
            self._serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.last_error = ""
            print(f"[ArduinoService] Connected to Arduino on {self.port}.")
            return True
        except Exception as exc:
            self._serial = None
            self.last_error = f"Arduino connection failed on {self.port}: {exc}"
            self._fallback_to_mock = True
            print(f"[ArduinoService] {self.last_error}. Falling back to mock mode.")
            return False

    def disconnect(self) -> None:
        """Close the serial connection if one is open."""
        if self.is_connected:
            try:
                self._serial.close()
                print("[ArduinoService] Arduino serial connection closed.")
            except Exception as exc:
                self.last_error = f"Arduino disconnect failed: {exc}"
                print(f"[ArduinoService] {self.last_error}")
        elif self.is_mock:
            print("[ArduinoService] Mock mode disconnected.")

        self._serial = None

    def send_vehicle_count(self, car: int, bus: int, truck: int, van: int) -> str:
        """Send LEVEL,CAR,BUS,TRUCK,VAN,TOTAL to Arduino or log it in mock mode."""
        car_count = self._clean_count(car)
        bus_count = self._clean_count(bus)
        truck_count = self._clean_count(truck)
        van_count = self._clean_count(van)
        total = car_count + bus_count + truck_count + van_count
        level = self.get_traffic_level(total)
        payload = f"{level},{car_count},{bus_count},{truck_count},{van_count},{total}"

        self.last_level = level
        self.last_sent_data = payload

        if not self.mock_mode and not self._fallback_to_mock and not self.is_connected:
            self.connect()

        if self.is_mock:
            print(f"[ArduinoService] Mock send: {payload}")
            return payload

        try:
            self._serial.write(f"{payload}\n".encode("utf-8"))
            self._serial.flush()
            print(f"[ArduinoService] Sent: {payload}")
        except Exception as exc:
            self.last_error = f"Arduino send failed: {exc}"
            self._fallback_to_mock = True
            try:
                self._serial.close()
            except Exception:
                pass
            self._serial = None
            print(f"[ArduinoService] {self.last_error}. Mock send: {payload}")

        return payload

    def get_traffic_level(self, total: int) -> str:
        """Return G, Y, or R for the current vehicle total."""
        total_count = self._clean_count(total)
        if total_count < 10:
            return "G"
        if total_count < 20:
            return "Y"
        return "R"

    def _clean_count(self, value: int) -> int:
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return 0

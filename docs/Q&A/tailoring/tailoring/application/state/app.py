'''
This file contains the general app state
'''

# app/state.py
import datetime as dt
import reflex as rx
from ..models import InviteCode, Response

class AppState(rx.State):
    # gate
    code_input: str = ""
    authed: bool = False
    active_code: str = ""

    # form fields
    name: str = ""
    email: str = ""
    feedback: str = ""
    message: str = ""

    def check_code(self):
        with rx.session() as s:
            ic = (
                s.query(InviteCode)
                 .filter(InviteCode.code == self.code_input)
                 .one_or_none()
            )
            now = dt.datetime.utcnow()
            if (
                ic is None or
                (ic.expires_at and ic.expires_at < now) or
                ic.used_at is not None
            ):
                self.message = "Invalid or already-used code."
                return
            # mark as reserved so two tabs can't reuse it later
            ic.used_at = now
            s.add(ic); s.commit()
            self.authed = True
            self.active_code = ic.code
            self.message = ""

    def submit(self):
        if not self.authed:
            self.message = "Please enter a valid code."; return
        with rx.session() as s:
            s.add(Response(code=self.active_code,
                           q_name=self.name,
                           q_email=self.email,
                           q_feedback=self.feedback))
            s.commit()
        self.authed = False
        self.active_code = ""
        self.name = self.email = self.feedback = ""
        self.message = "Thanks! Your response was recorded."

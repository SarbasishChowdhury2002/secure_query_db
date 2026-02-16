# ==============================
# Role-Based Access Control (RBAC)
# ==============================

class RBAC:
    def __init__(self):
        # Role → allowed actions
        self.permissions = {
            "admin": {"search", "read", "decrypt"},
            "analyst": {"search", "read"},
            "auditor": {"search"},
            "user": {"search"}
        }

    # --------------------------
    # Authorization Check
    # --------------------------
    def authorize(self, role: str, action: str) -> bool:
        """
        Check if role is allowed to perform action
        """
        if role not in self.permissions:
            return False

        return action in self.permissions[role]

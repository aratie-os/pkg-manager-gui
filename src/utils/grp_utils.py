import grp


class GroupUtils:

    @classmethod
    def is_user_in_group(cls, username: str, group: str) -> bool:
        try:
            flatpak_group_info = grp.getgrnam(group)
            group_members = flatpak_group_info.gr_mem

            if username in group_members:
                return True
            else:
                return False

        except KeyError:
            print(f"Aviso: O grupo 'flatpak' não foi encontrado no sistema.")
            return False
        except Exception as e:
            print(f"Ocorreu um erro ao verificar o grupo: {e}")
            return False

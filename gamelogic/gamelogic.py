"""
游戏逻辑模块
"""

import random
from collections import Counter

"""
游戏角色配置表硬编码
"""

config_list = [{},  # 0
               {},  # 1
               {},  # 2
               {},  # 3
               {'Villager': 1, 'Seer': 1, 'Witch': 1, 'Hunter': 0, 'Werewolf': 1},  # 4
               {'Villager': 2, 'Seer': 1, 'Witch': 0, 'Hunter': 0, 'Werewolf': 2},  # 5
               {'Villager': 2, 'Seer': 1, 'Witch': 1, 'Hunter': 0, 'Werewolf': 2},  # 6
               {'Villager': 3, 'Seer': 1, 'Witch': 1, 'Hunter': 0, 'Werewolf': 2},  # 7
               {'Villager': 3, 'Seer': 1, 'Witch': 1, 'Hunter': 0, 'Werewolf': 3},  # 8
               {'Villager': 3, 'Seer': 1, 'Witch': 1, 'Hunter': 1, 'Werewolf': 3},  # 9
               ]


# 角色类
class Character(object):
    def __init__(self):
        # self.id = 0  # 是否需要id
        self.status = "alive"  # alive, killed, poisoned,
        self.eye = 'open'  # 是否需要眼睛的状态
        self.hand = 'none'  # 手的状态


class Villager(Character):  # 村民
    def __init__(self):
        super().__init__()


class Seer(Character):  # 预言家
    def __init__(self):
        super().__init__()

    @staticmethod
    def see(player):
        return type(player).__name__


class Witch(Character):  # 女巫
    def __init__(self):
        super().__init__()
        self.have_poison = True  # 毒药
        self.have_elixir = True  # 解药

    def poison(self, player):
        if self.have_poison is True:  # 有毒药
            player.status = 'poisoned'
            self.have_poison = False
        elif self.have_poison is False:  # 没有毒药
            pass

    def save(self, player):
        if self.have_elixir is True:  # 有解药
            player.status = 'alive'
            self.have_elixir = False
        elif self.have_poison is False:  # 没有解药
            pass


# class Hunter(Character):  # 猎人
#     def __init__(self):
#         super().__init__()


class Werewolf(Character):  # 狼人
    def __init__(self):
        super().__init__()

    # def kill(self):
    #     pass

    # def boom(self): # 爆狼
    #     self.alive = False
    #     pass


# 游戏管理类
class Game(object):
    def __init__(self):
        self.players = {}  # 玩家id-实例表
        self.spec_id = {'Seer': 0, 'Witch': 0, 'Werewolf': []}  # 特殊角色位置
        self.progress = {}  # 游戏进程表 {day: [killed_id, poisoned_id, save]}
        self.protect = 0  # 首刀保护id
        self.num_players = 0  # 游戏人数
        print('################\n初始化Gamelogic成功\n################')

    def get_id_list(self):
        """
        获取id-character表
        :return: id_list
        """
        id_list = {}
        for player_id, player in self.players.items():
            id_list[player_id] = type(player).__name__
        return id_list

    def get_character_list(self):
        """
        获取当前游戏角色个数统计表
        :return: character_list
        """
        character_list = {'Villager': 0, 'Seer': 0, 'Witch': 0, 'Hunter': 0, 'Werewolf': 0}
        for player_id, player in self.players.items():
            if player.status == 'alive':
                if type(player).__name__ == 'Villager':
                    character_list['Villager'] += 1
                elif type(player).__name__ == 'Seer':
                    character_list['Seer'] += 1
                elif type(player).__name__ == 'Witch':
                    character_list['Witch'] += 1
                elif type(player).__name__ == 'Hunter':
                    character_list['Hunter'] += 1
                elif type(player).__name__ == 'Werewolf':
                    character_list['Werewolf'] += 1
                else:
                    return 0  # 角色统计列表返回失败
        return character_list

    def get_status_list(self):
        """
        获取id-status表 {id: status} status: alive, killed, poisoned
        :return: alive_list
        """
        status_list = {}
        for player_id, player in self.players.items():
            status_list[player_id] = player.status
        return status_list

    def start_game(self, num_players):
        """
        游戏初始化
        :param num_players: 游戏人数
        :return:
        """

        # 根据狼人杀配置表初始化游戏
        self.num_players = num_players

        character_list = []  # id顺序的角色列表
        # 按照顺序赋予每个id一个初始角色
        for character, num_character in config_list[num_players].items():
            while num_character > 0:
                character_list.append(character)
                num_character -= 1

        random.shuffle(character_list)  # 洗乱角色

        id_index = 1
        # 角色实例化
        for character in character_list:
            if character == 'Villager':
                self.players[id_index] = Villager()
            elif character == 'Seer':
                self.players[id_index] = Seer()
            elif character == 'Witch':
                self.players[id_index] = Witch()
            elif character == 'Hunter':
                pass
            elif character == 'Werewolf':
                self.players[id_index] = Werewolf()
            else:
                return 0  # 角色实例化失败
            id_index += 1

        # 记录特殊角色位置
        for player_id, player in self.players.items():
            if type(player).__name__ == 'Villager':
                pass
            elif type(player).__name__ == 'Seer':
                self.spec_id['Seer'] = player_id
            elif type(player).__name__ == 'Witch':
                self.spec_id['Witch'] = player_id
            elif type(player).__name__ == 'Hunter':
                pass
            elif type(player).__name__ == 'Werewolf':
                self.spec_id['Werewolf'].append(player_id)
            else:
                return 0  # 角色统计列表返回失败

        # 测试输出
        print('游戏初始化完成')
        for player_id, player in self.players.items():
            print(str(player_id) + '号玩家: ' + type(player).__name__)
        print('特殊角色位置')
        print(self.spec_id)

    def movement_werewolf(self, day, killed_id):
        """
        狼人行动
        :param day:
        :param killed_id:
        :return:
        """
        # 发送给狼人信息

        # 狼人杀人
        if self.players[killed_id].status == 'alive':  # 被杀的人存活
            self.players[killed_id].status = 'killed'
            self.progress[day] = [killed_id]  # 被杀的人存档
        else:
            pass  # 错误输出

    def movement_seer(self, see_id):
        """
        预言家行动
        :param see_id:
        :return:
        """
        seer = self.players[self.spec_id['Seer']]  # 找到预言家实例

        # 给预言家发送信息

        # 预言家验人
        res = seer.see(self.players[see_id])
        if res == 'Villager' or res == 'Seer' or res == 'Witch':
            print(str(see_id) + 'good person')
        else:
            print(str(see_id) + 'bad person')

    def movement_witch(self, day, poison_id, save):
        """
        女巫行动
        :param day:
        :param poison_id:
        :param save:
        :return:
        """
        witch = self.players[self.spec_id['Witch']]  # 找到女巫实例

        # 毒人流程
        if witch.have_poison is True and self.players[poison_id].status == 'alive':  # 毒死存活的人
            witch.poison(self.players[poison_id])
            self.progress[day].append(poison_id)  # 被毒的人存档
        else:
            self.progress[day].append(0)  # 没有人被毒

        # 救人流程
        if witch.have_elixir is True and save != 0:  # 女巫有药且决定救人
            save_id = self.progress[day][0]  # 今晚被杀的人
            witch.save(self.players[save_id])  # 救人
            self.progress[day].append(1)  #
        else:
            self.progress[day].append(0)  # 没有人被救

    def start_night(self):
        # 晚上流程初始化

        # 狼人行动
        pass

    def announce_night(self, day):
        """
        宣布晚上的结果
        :param day: 天数
        :return: [killed_id, poisoned_id] (0为无人)
        """
        announce = []
        if self.progress[day][2] == 1:  # 女巫救人
            announce.append(0)  # 被杀的人没有死
        elif self.progress[day] == 0:  # 女巫没有救人
            announce.append(self.progress[day][0])
        else:
            pass  # 错误输出

        announce.append(self.progress[day][1])  # 女巫毒人id

        return announce

    def voting(self):
        # 白天投票
        pass

    @staticmethod
    def is_gameover(character_list):
        """
        游戏结束判断
        :param character_list: 角色数量统计表
        :return: 0：游戏继续
                 1：好人获胜
                 2：狼人获胜
        """
        if character_list['Villager'] == 0 or character_list['Seer'] + character_list['Witch'] == 0:  # 屠边
            return 2
        elif character_list['Werewolf'] == (
                character_list['Villager'] + character_list['Seer'] + character_list['Witch']):  # 狼刀领先
            return 2
        elif character_list['Werewolf'] == 0:
            return 1
        else:
            return 0

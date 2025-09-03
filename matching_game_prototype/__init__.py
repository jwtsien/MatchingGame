from otree.api import *
from matching_game_prototype.population import Population
from matching_game_prototype.bidsrc import load_bid_function


doc = """
App: Players providd bid function code and the system will do match and show the results.
"""


class C(BaseConstants):
    NAME_IN_URL = 'matching_game_prototype'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 5


class Subsession(BaseSubsession):
    # introduced = models.LongStringField()
    match_result = models.LongStringField()
    unmatch_result = models.LongStringField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    bid = models.LongStringField(
        # label="Please enter you bid function (Ex: def bid(player, x, surplus): return x * surplus)"
    )

class InputBid(Page):
    form_model = "player"
    form_fields = ["bid"]

class WaitForBid(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(group: Group):
        subsession = group.subsession
        # Initialize population
        if subsession.round_number == 1:
            subsession.session.vars['the_population'] = Population(P=2)

        the_population: Population = subsession.session.vars['the_population']
        players = group.get_players()

        # Relod the bid_functions provided by the players
        func1 = load_bid_function(players[0].bid)
        func2 = load_bid_function(players[1].bid)

        half = the_population.I // 2
        # The first half agents use the first bid function
        for idx in range(half):
            the_population.bid_functions[int(the_population.p_i[idx])] = func1
        # The second half agents use the second bid function
        for idx in range(half, the_population.I):
            the_population.bid_functions[int(the_population.p_i[idx])] = func2

        # update the matching
        the_population.update()

        # restore the results to display
        subsession.match_result = str(list(the_population.matched))
        subsession.unmatch_result = str(list(the_population.unmatched))


class ShowMatch(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_num=player.subsession.round_number,
            match_result=player.subsession.match_result,
            unmatch_result=player.subsession.unmatch_result,
        )


page_sequence = [InputBid, WaitForBid, ShowMatch]

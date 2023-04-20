
class RunnerAdvance:
    def __init__(self, run_description, runner, start_base, end_base,
                 runner_scored, run_earned, is_rbi):
        self.run_description = run_description
        self.runner = runner
        self.start_base = start_base
        self.end_base = end_base
        self.runner_scored = runner_scored
        self.run_earned = run_earned
        self.is_rbi = is_rbi

    def _asdict(self):
        return (
            {'run_description': self.run_description,
             'runner': self.runner._asdict(),
             'start_base': self.start_base,
             'end_base': self.end_base,
             'runner_scored': self.runner_scored,
             'run_earned': self.run_earned,
             'is_rbi': self.is_rbi}
        )
    def __repr__(self):
        score_str = ''
        if self.runner_scored:
            score_str += '(Scored'

        if self.run_earned:
            score_str += ', Earned'

        if self.is_rbi:
            score_str += ', RBI'

        if self.runner_scored:
            score_str += ')'

        return_str = '- {:21} {:19} {:2}--->{:2} {:>21}'.format(
            str(self.runner) + ':',
            self.run_description,
            self.start_base,
            self.end_base,
            score_str
        )

        return return_str

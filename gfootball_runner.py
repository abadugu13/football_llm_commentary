from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from absl import logging

from playsound import playsound
from tortoise.utils.audio import load_audio

from gfootball.env import config
from gfootball.env import football_env

from commentary_pipeline import commentary_pipeline


FLAGS = flags.FLAGS

flags.DEFINE_string('players', '',
                    'Semicolon separated list of players, single keyboard '
                    'player on the left by default')
flags.DEFINE_string('level', '', 'Level to play')
flags.DEFINE_enum('action_set', 'default', ['default', 'full'], 'Action set')
flags.DEFINE_bool('real_time', True,
                  'If true, environment will slow down so humans can play.')
flags.DEFINE_bool('render', True, 'Whether to do game rendering.')


def main(_):
  players = FLAGS.players.split(';') if FLAGS.players else ''
  assert not (any(['agent' in player for player in players])
             ), ('Player type \'agent\' can not be used with play_game.')
  cfg_values = {
      'action_set': FLAGS.action_set,
      'dump_full_episodes': True,
      'players': players,
      'real_time': FLAGS.real_time,
  }
  if FLAGS.level:
    cfg_values['level'] = FLAGS.level
  cfg = config.Config(cfg_values)
  env = football_env.FootballEnv(cfg)
  previous_observation = None

  if FLAGS.render:
    env.render()
  env.reset()
  try:
    while True:
      observation, _, done, _ = env.step([])
      if previous_observation is None:
        previous_observation = observation
      comment, audio_path = commentary_pipeline(observation, previous_observation)
      if comment:
        print(comment)
      if audio_path:
        # play audio
        playsound(audio_path)

      previous_observation = observation
      if done:
        env.reset()
  except KeyboardInterrupt:
    logging.warning('Game stopped, writing dump...')
    env.write_dump('shutdown')
    exit(1)


if __name__ == '__main__':
  app.run(main)
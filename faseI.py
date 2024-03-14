#Pergunta 1: Qual o percentual de jogos gratuitos e pagos na plataforma?
#Pergunta 2: Qual o ano com o maior número de novos jogos? Em caso de empate, retorne uma lista com os anos empatados.
#Pergunta 3: Qual o percentual de jogos em inglês na plataforma?

import csv
import functools
from datetime import datetime

def get_only_year(str_date):
  try:
    date = datetime.strptime(str_date, '%b %d, %Y')
    return date.year
  except:
    date = datetime.strptime(str_date, '%b %Y')
    return date.year

def increment_if(condition):
  return lambda acc, game: acc + 1 if len(game) > 6 and condition(game[6]) else acc

def increment_if_lang_exists(lang):
  return lambda acc, game: acc + 1 if len(game) > 9 and lang in game[9] else acc


class Games:
  def __init__(self, source):
    self.games = []

    with open(source) as csvfile:
      csv_reader = csv.reader(csvfile)
      next(csv_reader)

      for row in csv_reader:
        self.games.append(row);

      #prints para visualizar as linhas e facilitar a identicar as posições.
      print(self.games[0])
      print(self.games[1][9])

  def free_games(self):
    return functools.reduce(increment_if(lambda price: price == '0.0'), self.games, 0)

  def paid_games(self):
    return functools.reduce(increment_if(lambda price: price != '0.0'), self.games, 0)

  def year_with_most_released_games(self):
    years_and_games = functools.reduce(lambda acc, game: {get_only_year(game[2]): acc.get(get_only_year(game[2]), 0) + 1}, self.games, {});
    max_year = max(years_and_games, key=years_and_games.get)
    tie_years = [year for year, count in years_and_games.items() if count == years_and_games[max_year]]

    if len(tie_years) == 1:
      return max_year
    else:
      return tie_years

  def english_games(self):
    return functools.reduce(increment_if_lang_exists('English'), self.games, 0)

def percent_of(total, slice):
  return (slice * 100) / total

games = Games('steam_games.csv');
#Qual o percentual de jogos gratuitos e pagos na plataforma?
percent_free = percent_of(len(games.games), games.free_games())
percent_paid = percent_of(len(games.games), games.paid_games())
print(f'Percentual de jogos oferecidos gratuitamente pela empresa Fun Corp: {round(percent_free)}%')
print(f'Percentual de jogos pagos oferecidos pela empresa Fun Corp: {round(percent_paid)}%')
print('Em resumo, os resultados dessa empresa de jogos refletem uma estratégia que valoriza a ampla distribuição e o engajamento da comunidade por meio de jogos gratuitos, enquanto também reserva um espaço para jogos pagos que atendem a uma demanda específica de jogadores dispostos a investir em experiências de jogo premium.')

#Qual o ano com o maior número de novos jogos? Em caso de empate, retorne uma lista com os anos empatados.
result = games.year_with_most_released_games()
if isinstance(result, list):
  print(f"Empate! Anos com o maior número de novos jogos: {result}")
else:
  print(f"O ano com o maior número de novos jogos é: {result}")

#Qual o percentual de jogos em inglês na plataforma?
percent_english = percent_of(len(games.games), games.english_games())
print(f'Percentual de jogos oferecidos em inglês pela empresa Fun Corp: {round(percent_english)}%')



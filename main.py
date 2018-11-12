from GithubInfoCollector import GithubInfoCollector


url='https://github.com/RocketChat/Rocket.Chat'

infoCollector = GithubInfoCollector(url,'./data.json')
infoCollector.collectCurrentData()

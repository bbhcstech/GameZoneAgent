import psutil

class GetActiveGames:
    # Common game executables - you can expand this
    GAME_PROCESSES = [
        'steam.exe',
        'epicgameslauncher.exe',
        'valorant.exe',
        'csgo.exe', 
        'dota2.exe',
        'fortnite.exe',
        'minecraft.exe',
        'rocketleague.exe',
        'gta5.exe',
        'rdr2.exe',
        'cod.exe',
        'battlefield.exe',
        'overwatch.exe',
        'apex.exe',
        'pubg.exe',
        'roblox.exe',
        'leagueoflegends.exe',
        'legends of runeterra.exe',
        'gog galaxy.exe'
    ]
    
    def execute(self, payload=None):
        try:
            active_games = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    # Check if this process is a known game
                    for game in self.GAME_PROCESSES:
                        if game.lower() in proc_name:
                            active_games.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cpu': round(proc.info['cpu_percent'] or 0, 1),
                                'memory': round(proc.info['memory_percent'] or 0, 1)
                            })
                            break
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                'success': True,
                'count': len(active_games),
                'games': active_games
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
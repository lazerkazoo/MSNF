curl -s "https://api.modrinth.com/v2/search?query=$1&limit=5&facets=%5B%5B%22project_type%3Aplugin%22%5D%2C%5B%22categories%3Apaper%22%5D%2C%5B%22versions%3A$2%22%5D%5D"

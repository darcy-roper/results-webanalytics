
import requests


event_group = ["sprints", "middle-long", "road-running", "hurdles", "throws", "jumps", "combined-events", "race-walks", "relays"]

sprints_ev = ["100-meters", "200-meters", "400-meters"]
mid_long_ev = ["800-meters", "1500-meters", "3000-metres-steeplechase", "5000-meters", "10000-meters"]
marathon_ev = ["marathon"]
hurdles_ev = ["110-meters-hurdles", "400-meters-hurdles"]
jumps_ev = ["long-jump", "triple-jump", "high-jump", "pole-vault"]
throws_ev = ["discus-throw", "shot-put", "javelin-throw", "hammer-throw"]
combined_ev = ["decathlon"]
walks_ev = ["10000-meters-race-walk", "20-kilometres-race-walk"]
relays_ev = ["4x100-metres-relay"]

sex = "men"
group = "sprints"  # this should be a variable which iterates through the event_group options
event = "400-meters"  # should iterate through events based on event group
ctry = "aus"


url = "https://worldathletics.org/records/toplists/"+group+"/"+event+"/outdoor/"+sex+"/senior/2022?regionType=countries&region="+ctry+"&timing=electronic&windReading=regular&page=1&bestResultsOnly=true"

headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'Connection': 'keep-alive',
  'Cookie': '__RequestVerificationToken=J2n6pg-L2FlBwkbEUbCu_r4-l1sDOgDHaQHbrPPdGpsSbiTJToWq9HIz3ZbHWOqDepwrg6ru0hxJwsnDtGV402_zDqYDyMQETsUpz46nDWQ1; NEXT_LOCALE=en; iaaf-cookie-banner=true; CookieConsent={stamp:%274bHa3WwGMCX1s3lm9x9duPywedfjpnLJBT98jg/Be2weIi/i/QxpWQ==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:false%2Cver:1%2Cutc:1666433990320%2Cregion:%27au%27}; _hjSessionUser_1590279=eyJpZCI6ImQxNmRmMzNiLTUzNjgtNWMxNy05ZTM2LTlmZTU2N2Y5OGQ0YSIsImNyZWF0ZWQiOjE2NjY0MzM5ODc3NDQsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_505088=eyJpZCI6IjMwZjMxMmZlLTdiNjQtNWQ3ZS1iYWY0LTcxZmUzYmE3ZmI0NSIsImNyZWF0ZWQiOjE2NjY1MjQxMzQ5MTUsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.973389510.1667087123; _hjIncludedInSessionSample=0; _hjSession_505088=eyJpZCI6ImRkNGUwMmVjLTBjNjQtNDhmYi04NWM3LTNmNjM4MzI1MDBhYyIsImNyZWF0ZWQiOjE2NjcxMTM0MjAxNTIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gat_UA-17416596-1=1; _ga_7FE9YV46NW=GS1.1.1667113420.15.0.1667113420.0.0.0; _ga=GA1.1.1996384928.1666433987',
  'Referer': "https://worldathletics.org/records/toplists/"+group+"/"+event+"/outdoor/"+sex+"/senior/2022?regionType=countries&region="+ctry+"&timing=electronic&windReading=regular&page=1&bestResultsOnly=true",
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-GPC': '1',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest'
}

response = requests.get(url, headers=headers)

print(response.text)


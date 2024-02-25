from datetime import datetime
import requests
import json
import uuid
import time as tt


def metatrader_import(inputid, inputpassword, inputtype, inputpassphrase):
    "type message 'connecting account from metatrader'"
    login = inputid
    password = inputpassword
    meta_type = inputtype
    passphrase = inputpassphrase
    headers = {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0NjdmNDc0YWIzMzk3ZmQ0NTZjMWU0YzFlYzE1YmEzMiIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjQ2N2Y0NzRhYjMzOTdmZDQ1NmMxZTRjMWVjMTViYTMyIiwiaWF0IjoxNzA3NjY4MDI4fQ.UpXWWnXzBQ0r1-FzmAg0dRvE_n4X7MdftJsl2kKvlmooF8oUWrJqibtAo-F2Kq2n4uUAePoTXuefgC53Cg1K1jnhfsNSgJO640OV4y38bGRGc_ezDP3fcW_6yq2RD1gxdt_Z4Ntw6oZUj7DLyw9gvhV0nL9-m0wN-z1X5F_hnaWbd_Q_3oNlP3r1Kk5gDwnyS3F8iYc6fimVcYp0b-m9yeKGgEKu40Ce14Rq7eRoqEZozeYoU1owWldFBD-xDA6CWl9aoT7ODH6x4Mc9AFcorsbxTl9UmyR5thmzr8DpV2OWeQlAK7VFmJ1L8d9Ih08XrSZYhX5tetfUXZlL-sdeqYH67Rn5LBMIfGyt1PxEQpSL8OuZfdB4vO6lm6fEYne2T0h6qjVNVYXTu03U_NdxGM9ShsW71i_08wYpv0AV3z4MRTB0DTFXmz3E2NzxSbCMJNMkIyggrIU8DvF3IUifkFHmLTwZI2U7igMIGf45CcFUDPdD0jaiiqP4tJc-xPl17ZTE5ZINzG0_yRWpKv8B8VX9egnJ65RTvYqdUDNyZtuM9kXgFT23KaXQs7MdfwuDv1yQDr-CHSMVLHVHduSrj0h0FnEc8ojvYn628fZG8eaj70srY6Gk_LueQTh8s8rRZHUQjPW6_R3UVTep9XaYUHdwaNGH8eTYa7FgJOGax9E"
        # "instrument":'SPX500_USD'
    }
    symbol_contract = {}
    # retrieve MetaApi MetaTrader account trades
    response = requests.request(
        "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts?offset=0&limit=1000&endpointVersion=v1", headers=headers).json()
    isCreated = False

    if response != []:
        for trade in response:
            if trade['login'] == login:
                isCreated = True
                account = trade['_id']
                symbols = requests.request(
                    "GET", "https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/"+account+"/symbols", headers=headers).json()
                for symbol in symbols:
                    symbol_info = requests.request(
                        "GET", "https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/"+account+"/symbols/"+symbol+"/specification", headers=headers).json()
                    symbol_contract[symbol] = symbol_info["contractSize"]
                response = requests.request(
                    "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts/"+account, headers=headers).json()
                key = response['version']
                if key == 4:
                    meta_type = 'mt4'
                else:
                    meta_type = 'mt5'
                if response["state"] == "UNDEPLOYED":
                    requests.request("POST", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts/" +
                                     account+"/deploy?executeForAllReplicas=true", headers=headers)
                    cont = 0
                    response = requests.request(
                        "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts/"+account, headers=headers).json()
                    while response["connectionStatus"] != "CONNECTED" and cont != 20:
                        cont += 1
                        tt.sleep(40)
                        response = requests.request(
                            "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts/"+account, headers=headers).json()
                        if response["connectionStatus"] == "CONNECTED":
                            break
                break

    # servers=['GrowthNext-Demo','FinotiveMarkets-Live']
    if not isCreated:
        if passphrase and login and password and meta_type:
            params = {
                "name": 'test',
                "login": login,
                "server": passphrase,
                "application": "MetaApi",
                "region": "new-york",
                "reliability": "high",
                "resourceSlots": 1,
                "type": "cloud-g2",
                "metastatsApiEnabled": True,
                "magic": 0,
                "quoteStreamingIntervalInSeconds": 2.5,
                "manualTrades": False,
                "password": password,
                "platform": meta_type
            }

        data = json.dumps(params)

        res = json.loads(data)
        transaction = str(uuid.uuid4()).replace('-', '')
        headers = {
            "auth-token": "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0NjdmNDc0YWIzMzk3ZmQ0NTZjMWU0YzFlYzE1YmEzMiIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjQ2N2Y0NzRhYjMzOTdmZDQ1NmMxZTRjMWVjMTViYTMyIiwiaWF0IjoxNzA3NjY4MDI4fQ.UpXWWnXzBQ0r1-FzmAg0dRvE_n4X7MdftJsl2kKvlmooF8oUWrJqibtAo-F2Kq2n4uUAePoTXuefgC53Cg1K1jnhfsNSgJO640OV4y38bGRGc_ezDP3fcW_6yq2RD1gxdt_Z4Ntw6oZUj7DLyw9gvhV0nL9-m0wN-z1X5F_hnaWbd_Q_3oNlP3r1Kk5gDwnyS3F8iYc6fimVcYp0b-m9yeKGgEKu40Ce14Rq7eRoqEZozeYoU1owWldFBD-xDA6CWl9aoT7ODH6x4Mc9AFcorsbxTl9UmyR5thmzr8DpV2OWeQlAK7VFmJ1L8d9Ih08XrSZYhX5tetfUXZlL-sdeqYH67Rn5LBMIfGyt1PxEQpSL8OuZfdB4vO6lm6fEYne2T0h6qjVNVYXTu03U_NdxGM9ShsW71i_08wYpv0AV3z4MRTB0DTFXmz3E2NzxSbCMJNMkIyggrIU8DvF3IUifkFHmLTwZI2U7igMIGf45CcFUDPdD0jaiiqP4tJc-xPl17ZTE5ZINzG0_yRWpKv8B8VX9egnJ65RTvYqdUDNyZtuM9kXgFT23KaXQs7MdfwuDv1yQDr-CHSMVLHVHduSrj0h0FnEc8ojvYn628fZG8eaj70srY6Gk_LueQTh8s8rRZHUQjPW6_R3UVTep9XaYUHdwaNGH8eTYa7FgJOGax9E",
            "transaction-id": transaction
        }
        try:
            response = requests.request(
                "POST", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts", headers=headers, json=params).json()
            if 'error' in response:
                return {"error": "Error connecting account, please verify your credentials"}
            account = response['id']
            tt.sleep(30)
            # print('get spot order')
            headers = {
                "Content-Type": "application/json",
                "auth-token": "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0NjdmNDc0YWIzMzk3ZmQ0NTZjMWU0YzFlYzE1YmEzMiIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjQ2N2Y0NzRhYjMzOTdmZDQ1NmMxZTRjMWVjMTViYTMyIiwiaWF0IjoxNzA3NjY4MDI4fQ.UpXWWnXzBQ0r1-FzmAg0dRvE_n4X7MdftJsl2kKvlmooF8oUWrJqibtAo-F2Kq2n4uUAePoTXuefgC53Cg1K1jnhfsNSgJO640OV4y38bGRGc_ezDP3fcW_6yq2RD1gxdt_Z4Ntw6oZUj7DLyw9gvhV0nL9-m0wN-z1X5F_hnaWbd_Q_3oNlP3r1Kk5gDwnyS3F8iYc6fimVcYp0b-m9yeKGgEKu40Ce14Rq7eRoqEZozeYoU1owWldFBD-xDA6CWl9aoT7ODH6x4Mc9AFcorsbxTl9UmyR5thmzr8DpV2OWeQlAK7VFmJ1L8d9Ih08XrSZYhX5tetfUXZlL-sdeqYH67Rn5LBMIfGyt1PxEQpSL8OuZfdB4vO6lm6fEYne2T0h6qjVNVYXTu03U_NdxGM9ShsW71i_08wYpv0AV3z4MRTB0DTFXmz3E2NzxSbCMJNMkIyggrIU8DvF3IUifkFHmLTwZI2U7igMIGf45CcFUDPdD0jaiiqP4tJc-xPl17ZTE5ZINzG0_yRWpKv8B8VX9egnJ65RTvYqdUDNyZtuM9kXgFT23KaXQs7MdfwuDv1yQDr-CHSMVLHVHduSrj0h0FnEc8ojvYn628fZG8eaj70srY6Gk_LueQTh8s8rRZHUQjPW6_R3UVTep9XaYUHdwaNGH8eTYa7FgJOGax9E"
                # "instrument":'SPX500_USD'
            }
            response = requests.request(
                "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts/"+account, headers=headers).json()

            cont = 0

            while response["connectionStatus"] != "CONNECTED" and cont != 20:
                cont += 1
                """
                  if cont==6:
                      self.deleteAccount()
                      response = requests.request("POST", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts", headers=headers,json=params).json()
                      self.account=response['id']   
                  """
                tt.sleep(30)
                response = requests.request(
                    "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts/"+account, headers=headers).json()
                if response["connectionStatus"] == "CONNECTED":
                    "type message 'connection success'"
                    break
                if cont == 1:
                    response = requests.request(
                        "POST", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts", headers=headers, json=params).json()
                    account = response['id']
                    response = requests.request(
                        "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts/"+account, headers=headers).json()

        except Exception as err:
            "type message wrong creating the account"
            print(err)
            return {"error": "Error occured"}
    get_orders = get_metatrader_orders(login)
    if "value" in get_orders:
        trade_data = extract_data(get_orders["value"], login, symbol_contract)
        return {'trades': trade_data}
    else:
        return {"error": get_orders["error"]}


def get_metatrader_orders(inputid):
    login = inputid
    orders = []
    "type message 'Get orders from metatrader'"
    # print('get spot order')
    headers = {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI0NjdmNDc0YWIzMzk3ZmQ0NTZjMWU0YzFlYzE1YmEzMiIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19XSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjQ2N2Y0NzRhYjMzOTdmZDQ1NmMxZTRjMWVjMTViYTMyIiwiaWF0IjoxNzA3NjY4MDI4fQ.UpXWWnXzBQ0r1-FzmAg0dRvE_n4X7MdftJsl2kKvlmooF8oUWrJqibtAo-F2Kq2n4uUAePoTXuefgC53Cg1K1jnhfsNSgJO640OV4y38bGRGc_ezDP3fcW_6yq2RD1gxdt_Z4Ntw6oZUj7DLyw9gvhV0nL9-m0wN-z1X5F_hnaWbd_Q_3oNlP3r1Kk5gDwnyS3F8iYc6fimVcYp0b-m9yeKGgEKu40Ce14Rq7eRoqEZozeYoU1owWldFBD-xDA6CWl9aoT7ODH6x4Mc9AFcorsbxTl9UmyR5thmzr8DpV2OWeQlAK7VFmJ1L8d9Ih08XrSZYhX5tetfUXZlL-sdeqYH67Rn5LBMIfGyt1PxEQpSL8OuZfdB4vO6lm6fEYne2T0h6qjVNVYXTu03U_NdxGM9ShsW71i_08wYpv0AV3z4MRTB0DTFXmz3E2NzxSbCMJNMkIyggrIU8DvF3IUifkFHmLTwZI2U7igMIGf45CcFUDPdD0jaiiqP4tJc-xPl17ZTE5ZINzG0_yRWpKv8B8VX9egnJ65RTvYqdUDNyZtuM9kXgFT23KaXQs7MdfwuDv1yQDr-CHSMVLHVHduSrj0h0FnEc8ojvYn628fZG8eaj70srY6Gk_LueQTh8s8rRZHUQjPW6_R3UVTep9XaYUHdwaNGH8eTYa7FgJOGax9E"
        # "instrument":'SPX500_USD'
    }

    response = requests.request(
        "GET", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts?offset=0&limit=1000&endpointVersion=v1", headers=headers).json()
    if response != []:
        for trade in response:
            if trade['login'] == login:
                region = trade['region']
                account = trade['_id']
                key = trade['version']
                if key == 4:
                    meta_type = 'mt4'
                else:
                    meta_type = 'mt5'
                    break

    startDate = '2000-01-01'

    now = datetime.now()
    endDate = now.strftime('%Y-%m-%d')
    startHora = '%2000%3A00%3A00.000'
    endHora = '%2023%3A59%3A59.000'

    # url1='https://mt-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/'+self.account+'/history-deals/time/'+startDate+startHora+'/'+endDate+endHora+'?offset='+offset

    # url2='https://metastats-api-v1.new-york.agiliumtrade.ai/users/current/accounts/'+self.account+'/historical-trades/'+startDate+startHora+'/'+endDate+endHora+'?offset='+offset+'&updateHistory=true'

    url3 = 'https://mt-client-api-uzjylcntlrgwy9nc.new-york.agiliumtrade.ai/users/current/accounts/'+account+'/positions'

    try:
     # response = requests.request("POST", "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai/users/current/accounts", headers=headers,json=params).json()
     # r = requests.get(url="https://mt-client-api-uzjylcntlrgwy9nc.new-york.agiliumtrade.ai/users/current/accounts/"+self.account+"/connected",headers=headers).json()
        offset = 0
        paginated = True
        ordenesDeals = []
        paramQuery = {
            'limit': 2000,
            'offset': offset
        }
        while (paginated):
            r = requests.get(url='https://mt-client-api-v1.'+region+'.agiliumtrade.ai/users/current/accounts/'+account +
                             '/history-deals/time/'+startDate+startHora+'/'+endDate+endHora, headers=headers, params=paramQuery).json()
            offset += len(r)
            paramQuery = {
                'limit': 2000,
                'offset': offset
            }
            if r != []:
                for i in r:
                    ordenesDeals.append(i)
            else:
                paginated = False

        offset = 0
        paginated = True
        ordenesTrades = []
        paramQuery = {
            'limit': 2000,
            'offset': offset
        }
        while (paginated):
            r2 = requests.get(url='https://metastats-api-v1.'+region+'.agiliumtrade.ai/users/current/accounts/'+account+'/historical-trades/' +
                              startDate+startHora+'/'+endDate+endHora+'?updateHistory=true', headers=headers, params=paramQuery).json()
            if 'trades' in r2:
                offset += len(r2['trades'])
                paramQuery = {
                    'limit': 2000,
                    'offset': offset
                }
                if r2['trades'] != []:
                    for i in r2['trades']:
                        ordenesTrades.append(i)
                else:
                    paginated = False
            else:
                paginated = False

        """
            r3 = requests.get(url=url3,headers=headers).json()
            
            
            if r3 !=[]:
             for k in r3:
              orden={}
              if self.broker.broker_id==128: 
               orden['position']=k['id']
              else:
               orden['ticket']=k['id']
              orden['open_time']=k['time']
              orden['type']='Buy' if 'POSITION_TYPE_BUY' in k['type'] else 'Sell'
              orden['size']=str(k['volume']) 
              orden['item']=k['symbol']
              orden['open_price']=str(k['openPrice']) 
              orden['close_time']=k['updateTime'] if 'updateTime' in k else ''
              orden['closed_price']=str(k['currentPrice'])  if 'currentPrice' in k else ''
              orden['taxes']=str(k['taxes'])  if 'taxes' in k else '0.0'
              orden['profit']=str(k['profit'])
              orden['commission']=str(k['commission'])
              orden['swap']=str(k['swap'])
              orden['sl']=k['stopLoss'] if 'stopLoss' in k else 0
              orden['tp']=k['takeProfit'] if 'takeProfit' in k else 0
              self.orders.append(orden)
              """
        count = 0
        c = 0
        """
            if ordenesTrades !=[]:  
                self.orders=ordenesTrades
                self.save_files(file_type='json')
            if ordenesDeals !=[]: 
                self.orders=ordenesDeals                 
                self.save_files(file_type='json')
            self.orders=[]
            broker=self.get_broker_key()
            """
        if ordenesTrades != []:
            for i in ordenesTrades:
                count += 1
                c += 1
                "type message 'Get orders from metatrader'"
                try:
                    comission = 0.0
                    swap = 0.0
                    count = 0
                    countBuy = 0
                    openPrice = 0.0
                    countSell = 0
                    closePrice = 0.0
                    orden = {}
                    orden['id'] = str(i['_id']).split("+")[1]
                    if meta_type == 'mt5':
                        orden['position'] = i['positionId'] if "positionId" in i else ""
                    else:
                        orden['ticket'] = i['positionId'] if "positionId" in i else ""
                    orden['open_time'] = i['openTime']
                    orden['type'] = 'Buy' if 'DEAL_TYPE_BUY' in i['type'] else 'Sell'
                    orden['size'] = str(i['volume']) if "volume" in i else ""
                    orden['item'] = i['symbol'] if "symbol" in i else ""
                    orden['open_price'] = str(
                        i['openPrice']) if "openPrice" in i else ""
                    orden['close_time'] = i['closeTime']
                    orden['closed_price'] = str(
                        i['closePrice']) if "closePrice" in i else ""
                    orden['taxes'] = str(i['taxes']) if 'taxes' in i else '0.0'
                    if "marketValue" not in i:
                        continue
                    orden['profit'] = str(
                        i['marketValue']) if "marketValue" in i else ""
                except Exception as err:
                    # print(err)
                    pass
                if ordenesDeals != []:
                    for j in ordenesDeals:
                        if 'positionId' in j:
                            if orden['id'] == j['positionId'] and (j['entryType'] == "DEAL_ENTRY_OUT" or j['entryType'] == "DEAL_ENTRY_IN"):
                                count += 1
                                comission += float(j['commission'])
                                swap += float(j['swap'])
                                if j['entryType'] == "DEAL_ENTRY_IN":
                                    countBuy += 1
                                    openPrice += float(j['price'])
                                if j['entryType'] == "DEAL_ENTRY_OUT":
                                    countSell += 1
                                    closePrice += float(j['price'])
                                if count == 1:
                                    orden['magic'] = j['magic']
                                    orden['sl'] = j['stopLoss'] if 'stopLoss' in j else 0
                                    orden['tp'] = j['takeProfit'] if 'takeProfit' in j else 0
                                orden['commission'] = str(comission)
                                orden['swap'] = str(swap)
                    if 'commission' not in orden:
                        orden['commission'] = str(0.0)
                        orden['swap'] = str(0.0)
                    if openPrice != 0.0 and countBuy != 0:
                        orden['open_price'] = str(openPrice/countBuy)
                    if closePrice != 0.0 and countSell != 0:
                        orden['closed_price'] = str(closePrice/countSell)
                    orders.append(orden)

        return {"value": orders}

    except Exception as err:
        print(err)
        "type message 'Error when obtaining the orders, verify that your account is connected to the broker'"
        tt.sleep(5)
        return {"error": "Error when obtaining the orders, verify that your account is connected to the broker"}


def extract_data(orders, loginId, contract):
    return_value = []
    for trade in orders:
        if float(trade["profit"]) > 0:
            status = "WIN"
            if float(trade["open_price"]) > float(trade["closed_price"]):
                side = "SHORT"
            else:
                side = "LONG"
        else:
            status = "LOSS"
            if float(trade["open_price"]) < float(trade["closed_price"]):
                side = "SHORT"
            else:
                side = "LONG"
        instrument = '$' + trade["item"]
        if side == "LONG":
            action = "Buy"
            action_2 = "Sell"
        else:
            action = "Sell"
            action_2 = "Buy"
            trade['size'] = "-" + trade['size']
        contract_size = contract[trade["item"]]
        if contract_size >= 100:
            pips = (float(trade["closed_price"]) -
                    float(trade["open_price"])) * float(trade["size"]) * contract_size
        else:
            pips = (float(trade["closed_price"]) -
                    float(trade["open_price"])) * float(trade["size"]) * contract_size * contract_size
        return_value.append(
            {"account_id": loginId, "broker": "Metatrader", "trade_id": trade["id"], "status": status, "open_date": trade["open_time"], "symbol": instrument, "entry": trade["open_price"], "exit": trade["closed_price"], "size": trade["size"], "pips": str(format(pips, '.5f')), "ret_pips": str(format(float(trade["profit"]) / abs(pips), '.10f')), "ret": trade["profit"], "ret_percent": "0", "ret_net": str(format(float(trade["profit"]) + float(trade["commission"]) + float(trade["swap"]), '.10f')), "side": side, "setups": "", "mistakes": "", "subs": [{"action": action, "spread": "SINGLE", "type": "FOREX", "date": trade["open_time"], "size": str(abs(float(trade["size"]))), "position": trade["size"], "price": trade["open_price"]}, {"action": action_2, "spread": "SINGLE", "type": "FOREX", "date": trade["close_time"], "size": str(abs(float(trade["size"]))), "position": "0", "price": trade["closed_price"]}]})
    return return_value

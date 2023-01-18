import json

import pandas as pd


def get_logs(wd):
    logs = wd.get_log('performance')
    df = pd.DataFrame(logs)
    df.message = df.message.apply(lambda r: json.loads(r))
    df['webview'] = df.message.apply(lambda r: r.get('webview'))
    df.message = df.message.apply(lambda r: r.get('message'))
    df['method'] = df.message.apply(lambda r: r.get('method'))
    df['params'] = df.message.apply(lambda r: r.get('params'))
    df.drop(columns=['message'], inplace=True)
    df['requestId'] = df.params.apply(lambda r: r.get('requestId'))
    df['frameId'] = df.params.apply(lambda r: r.get('frameId'))
    df['type'] = df.params.apply(lambda r: r.get('type'))
    df['request'] = df.params.apply(lambda r: r.get('request'))
    df['response'] = df.params.apply(lambda r: r.get('response'))
    return df


def get_request_id(logs, src):
    data = [json.loads(log.get('message')).get('message') for log in logs]
    df = pd.json_normalize(data, max_level=3)
    return df.loc[(df['params.request.url'] == src), 'params.requestId'].squeeze()


def get_image_base64_string_from_url(wd, request_id):
    return wd.execute_cdp_cmd('Network.getResponseBody', {"requestId": request_id}).get('body')

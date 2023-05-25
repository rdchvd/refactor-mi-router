# refactor-mi-router
This project helps to communicate with Xiaomi router API to allow and deny devices access to the Internet.

### Set up instructions

To work with the project you should create `.env` file with at least `SECRET_KEY` value (all envs you can see in [.env-example](.env-example)). 

Source any it and then you are ready to go!


### Example of usage
```python

>>> MI_PASSWORD = "your-router-password"
>>> MI_USERNAME = "admin-or-any-other"
>>> MI_IP = "your-router-ip"

>>> from mi_router import MiRouter

>>> router = MiRouter(MI_IP)
>>> router.login(MI_USERNAME, MI_PASSWORD)

{"is_succeeded": true, "content": {"url": "/cgi-bin/luci/;stok=some-token/web/home", "token": "some-token", "code": 0}}

>>> router.get_full_devices_info()

{"is_succeeded": true, "content": {"mac": "some-mac1", "list": [{"mac": "some-mac1", "oname": "some-mac-name1", "isap": 0, "parent": "", "authority": {"wan": 1, "pridisk": 0, "admin": 1, "lan": 1}, "push": 0, "online": 1, "name": "some-mac-name1", "times": 0, "ip": [{"downspeed": "0", "online": "12122", "active": 1, "upspeed": "0", "ip": "some-ip"}], "statistics": {"downspeed": "0", "online": "182665", "upspeed": "0"}, "icon": "", "type": 1}, {"mac": "some-mac2", "oname": "some-mac-name2", "isap": 0, "parent": "", "authority": {"wan": 1, "pridisk": 0, "admin": 1, "lan": 1}, "push": 0, "online": 1, "name": "some-mac-name2", "times": 0, "ip": [{"downspeed": "133", "online": "34234", "active": 1, "upspeed": "146", "ip": "some-ip"}], "statistics": {"downspeed": "133", "online": "5466", "upspeed": "146"}, "icon": "", "type": 2}, {"mac": "some-mac-3", "oname": "some-mac-name3", "isap": 0, "parent": "", "authority": {"wan": 1, "pridisk": 0, "admin": 1, "lan": 1}, "push": 0, "online": 1, "name": "some-mac-name3", "times": 0, "ip": [{"downspeed": "0", "online": "564", "active": 1, "upspeed": "0", "ip": "some-ip"}], "statistics": {"downspeed": "0", "online": "232", "upspeed": "0"}, "icon": "", "type": 1}], "code": 0}}

>>> router.get_connected_mac_addresses()

['some-mac-2', 'some-mac-3']

>>> router.deny_network_for_all_devices()

{"is_succeeded": true, "content": null}

>>> router.allow_network_for_all_devices()

{"is_succeeded": true, "content": null}
```
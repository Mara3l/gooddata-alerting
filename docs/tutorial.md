# How To Create Alerts in GoodData

If you wish to set alerts for specific metrics or visualizations in GoodData, this tutorial will guide you through the process using the GoodData Python SDK.
Alerts enhance your monitoring capabilities for critical metrics and automate the notification process. This can assist you in preventing serious issues.
With the flexibility of the GoodData Python SDK, you aren't limited to one predefined solution; you can customize it to your heart's content.

## Prerequisites:

- GoodData Cloud and GoodData API token.
- Python virtual environment.
- S3 bucket (you can still create alerting without S3 bucket but you will have just limited capabilities).
- SMTP server to send emails (for example, Gmail).

## Disclaimer:

- It works *only* with visualization type *Headline*.

## Step 1: Install dependencies

```bash
# install all dependencies defined in requirements.txt 
$ pip install -r requirements.txt
```
## Step 2: Setup all environment variables

```bash
export GOODDATA_HOST='<gooddata-host>'
export GOODDATA_TOKEN='<gooddata-token>'
export GOODDATA_WORKSPACE_ID='<gooddata-workspace-id>'
export S3_ACCESS_KEY_ID='<s3-access-key-id>'
export S3_SECRET_ACCESS_KEY='<s3-secret-access-key'
export S3_BUCKET_NAME='<s3-bucket-name>'
export EMAIL_PASSWORD='<email-password>'
```

`Tip: You can find the GoodData host and GoodData workspace ID in the URL <GOODDATA_HOST>/dashboards/#/workspace/<GOODDATA_WORKSPACE_ID>.`
    
## Step 3: Define thresholds

```yaml
visualizations:
    - id: <visualization-id> # id of visualization
    column: <entity-id> # the number to watch, it is the name of column returned from GoodData pandas dataframe
    threshold: <threshold> # threshold number, for example 300    
    threshold_type: uptrends # threshold type can be 'uptrends' or 'downtrends'
    - id: <visualization-id> # id of visualization
    column: <entity-id> # the number to watch, it is the name of column returned from GoodData pandas dataframe
    threshold: <threshold> # threshold number, for example 4 
    threshold_type: downtrends # threshold type can be 'uptrends' or 'downtrends'
```

`Tip: You can find the GoodData visualization ID if you open Analytics Designer with a specific visualization: <GOODDATA_HOST>/analyze/#/<GOODDATA_WORKSPACE_ID>/<GOODDATA_VISUALIZATION_ID>/edit.`
    
## Step 4: Define time to run alerting

In the [gooddata_alerting.py](../gooddata_aleting.py), you can adjust your prefered time to run alerting.

```python
schedule.every().day.at("08:00").do(main)

while True:
schedule.run_pending()
time.sleep(1)
```

`Tip: if you preferer, you can also run it during cache invalidation.`

## Step 5: Run it! 🚀

```bash
$ python gooddata_alerting.py
```

## How does it work?

The best demonstation of the whole functionality is the following script:

```python
for new_id, new_item in new_dict.items():
    old_item = old_dict.get(new_id)
    
    if old_item:
        if new_item.notify and not old_item.notified_before:
            notification.send_email("Alert!", f"Visualization with id {new_item.id} has reached threshold!")
            new_item.notified_before = True
    
        if old_item.notified_before and new_item.notify:
            new_item.notified_before = True
    
        if old_item.notified_before and not new_item.notify:
            new_item.notified_before = False
    else:
        if new_item.notify:
            notification.send_email("Alert!", f"Visualization with id {new_item.id} has reached threshold!")
            new_item.notified_before = True
```

- `new_dict` contains all information about current "numbers" from GoodData.
- `old_item` contains all information about past "numbers" from GoodData, for example from yesterday.
- If there are no past "numbers", it sends a notification in case a visualization has reached a defined threshold.
- If there are past "numbers", it checks if a visualization has reached a defined threshold and if so, it will send a notification.
    - If notification was already sent, it does nothing.
    - If a visualization has dropped below a defined threshold, it resets a notification mechanism (to send a notification once a threshold will be reached again).
    
`Note: check also other things in `services` or `utils` but these are just let say regular Python stuff to make the whole alerting working.`

## Conclusion

If you have any queries or require assistance, don't hesitate to reach out on the GoodData Slack channel. Ready to get started? Explore the possibilities by signing up for our free trial today!
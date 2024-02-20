from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'callback' not in globals():
    from mage_ai.data_preparation.decorators import callback


@callback('success')
def trigger(parent_block_data, **kwargs):
    trigger_pipeline(
        'gcs_to_bq',        # Required: enter the UUID of the pipeline to trigger
        variables={},           # Optional: runtime variables for the pipeline
        check_status=False,     # Optional: poll and check the status of the triggered pipeline
        error_on_failure=False, # Optional: if triggered pipeline fails, raise an exception
        poll_interval=60,       # Optional: check the status of triggered pipeline every N seconds
        poll_timeout=None,      # Optional: raise an exception after N seconds
        verbose=True,           # Optional: print status of triggered pipeline run
    )

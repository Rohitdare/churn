def decide_execution(playbook, risk):
    """
    Decide how the agent executes an action.
    """

    if risk == "HIGH" and playbook["execution"] == "ONE_TO_ONE":
        return "EXECUTE_NOW"

    if playbook["execution"] == "BULK":
        return "QUEUE_FOR_BATCH"

    return "DEFER"

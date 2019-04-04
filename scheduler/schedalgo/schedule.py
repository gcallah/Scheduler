import json
from collections import Counter


def sched(data):
    data_dict = json.loads(data)
    consumers = data_dict['consumers']
    resourses = data_dict['resources']

    sched = make_sched(consumers, resourses)
    unsched = get_unsched(consumers, sched)

    ret_val = {}
    ret_val['scheduled'] = sched
    ret_val['unscheduled'] = unsched
    return json.dumps(ret_val)


def make_sched(consumers, resources):

    scheduled_consumers = []
    counter_cnt = Counter([c for c in consumers.keys()])

    for consumer_name, consumer in consumers.items():
        for type_resource in consumer['type']:
            resource = resources[type_resource]
            for resource_name, individ_resource in resource.items():

                scheduled_rnames = list(map(
                    lambda item: item['rname'], scheduled_consumers))
                scheduled_cnames = list(map(
                    lambda item: item['cname'], scheduled_consumers))

                tot_consumer_cnt = counter_cnt[consumer_name]
                sched_consumer_cnt = scheduled_cnames.count(consumer_name)

                if (resource_name not in scheduled_rnames
                        and tot_consumer_cnt != sched_consumer_cnt):

                    flag = True

                    for attribute in consumer:
                        if attribute in individ_resource:

                            op = individ_resource[attribute]['op_type']

                            cvalue = consumer[attribute]['value']
                            rvalue = individ_resource[attribute]['value']

                            match_fun = get_operation_function(op)

                            flag &= match_fun(rvalue, cvalue)

                    if flag:
                        scheduled_consumer = {
                            'rname': resource_name,
                            'cname': consumer_name,
                            'cattributes': consumer,
                            'rattributes': individ_resource,
                        }

                        scheduled_consumers.append(scheduled_consumer)

    return scheduled_consumers


def get_unsched(all_consumers, scheduled_consumers):
    unscheduled_consumers = []
    sched_consumer_names = [d['cname'] for d in scheduled_consumers]
    all_consumer_names = [d for d in all_consumers.keys()]

    for consumer in sched_consumer_names:
        try:
            all_consumer_names.remove(consumer)
        except ValueError:
            pass

    return all_consumer_names


def get_operation_function(op_type):

    if op_type == 'GE':
        return lambda x, y: x >= y
    elif op_type == 'eq':
        return lambda x, y: x == y
    elif op_type == 'le':
        return lambda x, y: x <= y
    else:
        raise RuntimeError("Operation Type Wrong!")
# -*- coding: UTF-8 -*-
# redis 里面使用列表和hash 表实现简单的任务队列
import redis
import json

client = redis.Redis(host='192.168.102.186', port=6379,db=0)

#添加任务
def add_task(task_id,target):
    task_detail = {'task_id':task_id,'target':target}
    client.hset('task_detail',task_id,json.dumps(task_detail))
    client.rpush('task_queue',task_id)

#发邮件读取任务
def read_task():
    # 因为返回的是一个元组('task_queue', '2'),所以要用下标进行取值
    task_id = client.blpop('task_queue')[1]
    task_detail = client.hget('task_detail',task_id)
    target = json.loads(task_detail)['target']
    print u'给 %s 发送邮件'%target

# 删除任务
def del_task(task_id):
    client.lrem('task_queue',0,task_id)
    client.hdel('task_detail',task_id)

# 暂停任务

def pause_task(task_id):
    client.lrem('task_queue',0,task_id)
    client.rpush('task_pause',task_id)


# 恢复任务

def resume_task(task_id):
    # 参数0代表的意思是移除表中所有与 value 相等的值。
    client.lrem('task_pause', 0, task_id)
    client.rpush('task_queue', task_id)



if __name__ == '__main__':
    # add_task(1,'www.baidu.com')
    # add_task(2, 'www.163.com')
    read_task()
    # pause_task(1)
    # resume_task(1)
<pre>
1、抓取知乎点赞数超过1000的问题及回答，并将其发送到邮箱或Evernote。
	(evernote普通用户接口，每天只能接收46条信息，并且每月总流量为60M)，后改为向163邮箱发送
	每封邮件中含20个问题(每个问题包含1~n个点赞数超过1000的回答)
2、知乎神回复，略显简单粗暴，字数在150字以内，点赞数超过500的回复

sys文件夹:
（1）cat_id_mapping_34.txt，话题广场的34个话题及其对应的id，用于抓取topic_id
（2）all_topic_id.txt，34个话题所对应的所有topic_id(共1524)(遍历34个id抓取topic_id耗时：16.4s)

data文件夹:
question_ids.txt文件
	所有词频大于500、回复字数在100以内的数据保存在humor_Q_A_old_version1.txt文件中
	所有词频大于500、回复字数在100-150的数据保存在humor_Q_A_old_version2.txt文件中
	
</pre>    


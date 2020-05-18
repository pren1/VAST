# import tensorflow as tf
# i = tf.constant(0)
# while_condition = lambda i: tf.less(i, 5)
# def body(i):
#     # do something here which you want to do in your loop
#     # increment i
#     return [tf.add(i, 1)]
#
# # do the loop:
# r = tf.while_loop(while_condition, body, [i])
#
# cost_matrix = tf.Variable(np.ones((LENGTH_MAX_OUTPUT+1, LENGTH_MAX_OUTPUT+1)), dtype=tf.float32)
#
# def iterate_batch(it_batch_nr, cost):
#     it_rows = tf.while_loop(while_condition, iterate_row, [it_row_nr])
#
# def iterate_row(it_row_nr):
#     a = tf.assign(cost_matrix[0,0], 100.0)
#     with tf.control_dependencies([a]):
#         return tf.add(it_row_nr,1)

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

tf_variable = tf.Variable(tf.constant(1))

def body(i, v):
    v_updated = i
    yield tf.add(i, 1), v_updated

_, updated = tf.while_loop(lambda i, _: tf.less(i, 100), body, [0, tf_variable])

with tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())
    # print(sess.run(tf_variable))
    print(sess.run(updated))
import numpy as np
from flask import Flask, jsonify, request

ITERATION_COUNT = 100


def direction(angle, segment_length):
    return segment_length * np.array((
        np.cos(angle),
        np.sin(angle),
    ))


def get_pos(angle_vec, segment_length_vec):
    return sum(
        direction(angle, segment_length)
        for angle, segment_length in zip(angle_vec, segment_length_vec)
    )


def jacobian_column(angle, segment_length):
    return segment_length * np.array((
        -np.sin(angle),
        np.cos(angle),
    ))


def jacobian(angle_vec, segment_length_vec):
    return np.column_stack(
        [jacobian_column(angle, segment_length) for angle, segment_length in
         zip(angle_vec, segment_length_vec)])


def ik3(segment_length_vec, x0, p1):
    last_x = x0

    for _ in range(ITERATION_COUNT):
        jk = jacobian(last_x, segment_length_vec)
        pseudo_inverse_jk = np.linalg.pinv(jk)

        pos = get_pos(last_x, segment_length_vec)
        error = p1 - pos
        if np.linalg.norm(error, ord=2) < 1e-6 ** 2:
            break

        last_x = last_x + pseudo_inverse_jk.dot(error)

    return list(last_x % (2 * np.pi))


app = Flask(__name__)


@app.route('/')
def hello_world():
    segment_length_vec = np.array([
        float(request.args.get('segment1')),
        float(request.args.get('segment2')),
        float(request.args.get('segment3')),
    ])

    p1 = np.array([
        float(request.args.get('posX')),
        float(request.args.get('posY')),
    ])

    x0 = np.array((0., 0., 0.))

    return jsonify(ik3(segment_length_vec, x0, p1))

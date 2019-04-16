import request from '@/utils/request'

export function autotaskList (params) {
  return request({
    url: '/api/autotask/',
    method: 'get',
    params
  })
}

export function createautotask (data) {
  return request({
    url: '/api/autotask/',
    method: 'post',
    data
  })
}

// 执行任务
export function updateautotask (id, data) {
  return request({
    url: '/api/autotask/' + id + '/',
    method: 'patch',
    data
  })
}

// 任务详情
export function detailautotask (id) {
  return request({
    url: '/api/autotask/' + id + '/',
    method: 'get'
  })
}

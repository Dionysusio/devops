import request from '@/utils/request'

// 获取申请列表
export function getDeployList (params) {
  return request({
    url: '/deploy/',
    method: 'get',
    params
  })
}

// 申请项目上线
export function createDeploy (data) {
  return request({
    url: '/deploy/',
    method: 'post',
    data
  })
}

// 更新项目
export function updateDeploy (id, data) {
  return request({
    url: '/deploy/' + id + '/',
    method: 'patch',
    data
  })
}

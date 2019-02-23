import request from '@/utils/request'

// 获取数据
export function getUserList(params) {
  return request({
    url: '/api/Users/',
    method: 'get',
    params
  })
}
// 修改的动作在api接口里定义方法,get请求数据在params里,剩下的在data里
export function getUser(userId) {
  return request({
    url: `/api/Users/${userId}/`,
    method: 'get'
  })
}

export function modifyUser(id, data) {
  return request({
    url: `/api/Users/${id}/`,
    method: 'patch',
    data
  })
}

export function changeUserStatus(id, data) {
  return request({
    url: `/api/Users/${id}/`,
    method: 'patch',
    data
  })
}

export function addUser(data) {
  return request({
    url: `/api/userReg/`,
    method: 'post',
    data
  })
}

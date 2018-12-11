import request from '@/utils/request'

export function getUserList(params) {
  return request({
    url: '/Users/',
    method: 'get',
    params
  })
}

export function changeUserStatus(pk, data) {
  return request({
    url: '/Users/' + pk + '/',
    method: 'patch',
    data
  })
}

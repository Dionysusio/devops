import request from '@/utils/request'

// 获取权限列表
export function getPermissionList (params) {
  return request({
    url: '/api/permission/',
    method: 'get',
    params
  })
}

// 更新指定用户组的权限列表
export function updateGroupPermissionList (gid, data) {
  return request({
    url: `/api/groupPermission/${gid}/`,
    method: 'patch',
    data
  })
}

// 获取指定用户组的权限列表
export function getGroupPermissionList (gid, params) {
  return request({
    url: `/api/groupPermission/${gid}/`,
    method: 'get',
    params
  })
}

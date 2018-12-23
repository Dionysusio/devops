import request from '@/utils/request'

export function getGroupList(params) {
  return request({
    url: '/api/groups/',
    method: 'get',
    params
  })
}

export function addGroup(data) {
  return request({
    url: '/api/groups/',
    method: 'post',
    data
  })
}

export function modifyGroup(id, data) {
  return request({
    url: `/api/groups/${id}/`,
    method: 'patch',
    data
  })
}

// 修改指定用户的角色
export function updateUserGroups(uid, data) {
  return request({
    url: `/api/userGroups/${uid}/`,
    method: 'patch',
    data
  })
}

// 获取指定用户的所有角色
export function getUserGroupList(uid, params) {
  return request({
    url: `/api/userGroups/${uid}/`,
    method: 'get',
    params
  })
}

// 获取指定用户组下的成员列表
export function getGroupMemberList(gid, params) {
  return request({
    url: `/api/groupMembers/${gid}/`,
    method: 'get',
    params
  })
}

// 从用户组中移除指定用户
export function removeGroupMember(gid, data) {
  return request({
    url: `/api/groupMembers/${gid}/`,
    method: 'delete',
    data
  })
}

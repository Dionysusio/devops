import request from '@/utils/request'

// 获取出版社列表
export function getAuthorList(params) {
  return request({
    url: '/api/author/',
    method: 'get',
    params
  })
}

// 修改作者信息
export function UpdateAuthor(id, data) {
  return request({
    url: `/api/author/${id}/`,
    method: 'put',
    data
  })
}

// 删除作者信息
export function DeleteAuthor(id) {
  return request({
    url: `/api/author/${id}/`,
    method: 'delete'
  })
}

// 添加作者信息
export function CreateAuthor(data) {
  return request({
    url: '/api/author/',
    method: 'post',
    data
  })
}

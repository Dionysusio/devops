<template>
  <div class="app-container">
    <el-row>
      <el-col :span="12">
        <el-input v-model="params.name" placeholder="搜索用户组" @keyup.enter.native="handleSearch">
          <el-button slot="append" icon="el-icon-search" @click="handleSearch"/>
        </el-input>
      </el-col>
      <el-col :span="12" align="right" style="padding-right:20px;">
        <el-button type="primary" @click="handleAddGroup">增加用户组</el-button>
      </el-col>
    </el-row>
    <el-table
      :data="groupData"
      stripe
      style="width: 100%">
      <el-table-column
        type="index"
        width="50" />
      <el-table-column
        prop="name"
        label="姓名"/>
      <el-table-column
        fixed="right"
        label="成员管理">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleGroupMember(scope.row)">成员列表<el-badge :value="scope.row.members" class="mark" /></el-button>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        label="权限管理">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleGroupPermission(scope.row)">修改权限</el-button>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleModifyGroup(scope.row)">修改</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-row v-show="total>10" type="flex" justify="center" style="padding-top:20px;">
      <el-pagination
        :total="total"
        layout="prev, pager, next"
        background
        @current-change="handleChange" />
    </el-row>
    <GroupForm v-model="groupFormVisible" :gid="groupId" :gname="groupName" @fetch="handleFetch"/>
    <GroupMember v-model="groupMemberVisible" :gid="groupId" :gname="groupName" @fetch="handleFetch"/>
    <GroupPermission v-model="groupPermissionVisible" :gid="groupId" :gname="groupName"/>
  </div>
</template>
<script>
import { getGroupList } from '@/api/group'
import GroupForm from './components/groupForm'
import GroupMember from './components/groupMembers'
import GroupPermission from './components/groupPermission'
export default {
  name: 'Groups',
  components: {
    GroupForm,
    GroupMember,
    GroupPermission
  },
  data() {
    return {
      groupData: [],
      total: 0,
      params: {
        page: 1,
        name: ''
      },
      groupFormVisible: false,
      groupMemberVisible: false,
      groupPermissionVisible: false,
      groupId: 0,
      groupName: ''
    }
  },
  created() {
    this.fetchGroupList()
  },
  methods: {
    fetchGroupList() {
      getGroupList(this.params).then(res => {
        this.groupData = res.results
        this.total = res.count
      })
    },
    handleChange(val) {
      this.params.page = val
      this.fetchGroupList()
    },
    handleSearch() {
      this.params.page = 1
      this.fetchGroupList()
    },
    handleAddGroup() {
      this.groupId = 0
      this.groupName = ''
      this.groupFormVisible = true
    },
    handleFetch() {
      this.groupId = 0
      this.fetchGroupList()
    },
    handleModifyGroup(obj) {
      this.groupId = obj.id
      this.groupName = obj.name
      this.groupFormVisible = true
    },
    handleGroupMember(obj) {
      this.groupId = obj.id
      this.groupName = obj.name
      this.groupMemberVisible = true
    },
    handleGroupPermission(obj) {
      this.groupId = obj.id
      this.groupName = obj.name
      this.groupPermissionVisible = true
    }
  }
}
</script>

/**
 * Client Memory CRUD — LingoGrade
 * Requires: supabase-init.js (window.supabase)
 */
var ClientMemory = (function () {
  'use strict';

  var TABLE = 'client_memories';
  var CATEGORIES = ['observation', 'preference', 'trigger', 'progress', 'logistics', 'parent_note'];
  var PAGE_SIZE = 25;

  function db() {
    return window.supabase;
  }

  // ── List memories for a student ──
  function list(studentId, opts) {
    opts = opts || {};
    var query = db()
      .from(TABLE)
      .select('*')
      .eq('student_id', studentId)
      .order('is_pinned', { ascending: false })
      .order('created_at', { ascending: false });

    if (opts.category) query = query.eq('category', opts.category);
    if (opts.search) query = query.or('title.ilike.%' + opts.search + '%,body.ilike.%' + opts.search + '%');

    var page = opts.page || 0;
    query = query.range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1);

    return query;
  }

  // ── Get single memory ──
  function get(id) {
    return db().from(TABLE).select('*').eq('id', id).single();
  }

  // ── Create memory ──
  function create(entry) {
    return db().from(TABLE).insert({
      student_id:   entry.student_id,
      assessor_id:  entry.assessor_id,
      category:     entry.category,
      tags:         entry.tags || [],
      title:        entry.title,
      body:         entry.body,
      session_date: entry.session_date || null,
      is_pinned:    entry.is_pinned || false
    }).select().single();
  }

  // ── Update memory ──
  function update(id, changes) {
    return db().from(TABLE).update(changes).eq('id', id).select().single();
  }

  // ── Delete memory ──
  function remove(id) {
    return db().from(TABLE).delete().eq('id', id);
  }

  // ── Toggle pin ──
  function togglePin(id, currentPinned) {
    return update(id, { is_pinned: !currentPinned });
  }

  // ── Export all memories for a student (GDPR) ──
  function exportAll(studentId) {
    return db()
      .from(TABLE)
      .select('*')
      .eq('student_id', studentId)
      .order('created_at', { ascending: true });
  }

  // ── Delete all memories for a student (GDPR) ──
  function deleteAll(studentId) {
    return db().from(TABLE).delete().eq('student_id', studentId);
  }

  return {
    CATEGORIES: CATEGORIES,
    PAGE_SIZE: PAGE_SIZE,
    list: list,
    get: get,
    create: create,
    update: update,
    remove: remove,
    togglePin: togglePin,
    exportAll: exportAll,
    deleteAll: deleteAll
  };
})();

#include "archetype.h"

mg::Archetype::Archetype(
    const re::u32 component_count,
    const ComponentData* components,
    const re::u32 capacity
) : k_chunk_capacity(capacity) {
    re_assert(k_chunk_capacity > 0, "Cannot create an archetype with zero capacity!");
    re_assert(
        component_count > 0 &&
        components != nullptr,
        "Cannot create an archetype with no components!"
    );

    for (re::u32 idx = 0; idx < component_count; ++idx) {
        const ComponentData& component = components[idx];

        m_component_to_offset[component.id] = m_entity_size;
        m_entity_size += component.size;
    }

    m_chunk_data_size = k_chunk_capacity * m_entity_size;

    m_head = new ArchetypeChunk();
    m_head->data = new re::u8[m_chunk_data_size]{0U};
    m_head->entities = new EntityID[k_chunk_capacity];
    m_tail = m_head;
}

mg::Archetype::~Archetype() {
    ArchetypeChunk* temp = nullptr;

    while (m_head != nullptr) {
        temp = m_head->next;

        delete[] m_head->data;
        delete[] m_head->entities;
        delete m_head;

        m_head = temp;
    }
}

mg::EntityID mg::Archetype::createEntity() {
    if (m_tail_size == k_chunk_capacity) {
        m_tail_size = 0;
        ++m_tail_index;

        m_tail->next = new ArchetypeChunk();
        m_tail->next->prev = m_tail;
        m_tail = m_tail->next;

        m_tail->data = new re::u8[m_chunk_data_size]{0U};
        m_tail->entities = new EntityID[k_chunk_capacity];
    }

    m_tail->entities[m_tail_size] = m_next_entity_id;
    m_entity_to_index[m_next_entity_id] = {
        .chunk_index = m_tail_index,
        .data_index = m_tail_size,
    };

    ++m_tail_size;

    return m_next_entity_id++;
}

void mg::Archetype::destroyEntity(const mg::EntityID entity_id) {
    re_assert(
        m_entity_to_index.find(entity_id) != m_entity_to_index.end(),
        "Invalid deletion of entity from archetype!"
    );

    ArchetypeChunkIndex entity_index = m_entity_to_index[entity_id];

    ArchetypeChunk* entity_chunk = m_head;
    for (re::u32 idx = 0; idx <= entity_index.chunk_index; ++idx) {
        entity_chunk = entity_chunk->next;
    }

    m_entity_to_index.erase(entity_id);
    --m_tail_size;

    EntityID last_entity = m_tail->entities[m_tail_size];
    entity_chunk->entities[entity_index.data_index] = last_entity;
    m_entity_to_index[last_entity] = entity_index;

    memcpy(
        &entity_chunk->data[entity_index.data_index * m_entity_size],
        &m_tail->data[m_tail_size * m_entity_size],
        m_entity_size
    );

    if (m_tail_size == 0 && m_tail != m_head) {
        ArchetypeChunk* temp = m_tail->prev;

        delete[] m_tail->data;
        delete[] m_tail->entities;
        delete m_tail;

        m_tail_size = k_chunk_capacity;
        m_tail = temp;
        m_tail->next = nullptr;
    }
}

#include "archetype.h"

mg::Archetype::Archetype(
    const re::u32 component_count,
    const ComponentData* components,
    const re::u32 capacity
) : k_chunk_capacity(capacity) {
    for (re::u32 idx = 0; idx < component_count; ++idx) {
        const ComponentData& component = components[idx];

        m_entity_size += component.size;

        // TODO: Setup component ordering map
    }

    m_chunk_data_size = k_chunk_capacity * m_entity_size;

    m_head = new ArchetypeChunk();
    m_head->data = new re::u8[m_chunk_data_size]{0U};
    m_tail = m_head;
}

mg::Archetype::~Archetype() {
    ArchetypeChunk* temp = nullptr;

    while (m_head != nullptr) {
        temp = m_head->next;

        delete[] m_head->data;
        delete m_head;

        m_head = temp;
    }
}

mg::EntityID mg::Archetype::createEntity() {
    if (m_tail_size == k_chunk_capacity) {
        m_tail_size = 0;

        m_tail->next = new ArchetypeChunk();
        m_tail = m_tail->next;

        m_tail->data = new re::u8[m_chunk_data_size]{0U};
    }

    ++m_tail_size;

    // TODO: Map entity to index/chunk

    return m_next_entity_id++;
}

void mg::Archetype::destroyEntity(const mg::EntityID entity_id) {
    // TODO: EVERYTHING
}

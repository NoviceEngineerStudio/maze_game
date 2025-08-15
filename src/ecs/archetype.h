#ifndef MG_SRC_ECS_ARCHETYPE_H
#define MG_SRC_ECS_ARCHETYPE_H

#include "components.h"
#include <unordered_map>

namespace mg {
    typedef re::u32 EntityID;

    class Archetype {
    public:
        Archetype(
            const re::u32 component_count,
            const ComponentData* components,
            const re::u32 capacity
        );

        ~Archetype();

        Archetype(const Archetype&) = delete;
        Archetype(Archetype&&) = delete;

        Archetype& operator=(const Archetype&) = delete;
        Archetype& operator=(Archetype&&) = delete;

        EntityID createEntity();
        void destroyEntity(const EntityID entity_id);

        // TODO: Add query iterator

    private:
        struct ArchetypeChunk {
            re::u8* data = nullptr;
            EntityID* entities = nullptr;

            ArchetypeChunk* prev = nullptr;
            ArchetypeChunk* next = nullptr;
        };

        struct ArchetypeChunkIndex {
            re::u32 chunk_index = 0;
            re::u32 data_index = 0;
        };

        std::unordered_map<ComponentID, re::u32> m_component_to_offset = {};

        re::u32 m_tail_size = 0;
        re::u32 m_tail_index = 0;
        ArchetypeChunk* m_tail = nullptr;
        ArchetypeChunk* m_head = nullptr;

        re::u32 m_entity_size = 0;
        re::u32 m_chunk_data_size = 0;
        const re::u32 k_chunk_capacity;

        EntityID m_next_entity_id = 0;
        std::unordered_map<EntityID, ArchetypeChunkIndex> m_entity_to_index = {};
    };
}

#endif
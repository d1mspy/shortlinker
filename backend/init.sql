create table if not exists link(
    id uuid primary key,
    created_at timestamp not null,
    updated_at timestamp not null,
    short_link text not null unique,
    long_link text not null
);

create table if not exists link_usage(
    id uuid primary key,
    created_at timestamp not null,
    updated_at timestamp not null,
    user_ip text not null,
    user_agent text not null,
    short_link text not null
);
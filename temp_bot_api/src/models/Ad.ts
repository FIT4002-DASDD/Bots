import {
  BaseEntity,
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  OneToMany,
  PrimaryGeneratedColumn,
  Unique,
} from "typeorm";
import { Bot } from ".";

@Entity()
export class Ad extends BaseEntity {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @ManyToOne(() => Bot, (bot) => bot.ads)
  @JoinColumn({ name: "botId" })
  bot?: Bot;

  @Column("uuid")
  botId?: string;

  @Column("timestamptz", {
    default: () => "CURRENT_TIMESTAMP",
  })
  createdAt!: Date;

  @Column("varchar", { nullable: true })
  image?: string;

  @Column("varchar", { nullable: true })
  headline?: string;

  @Column("varchar", { nullable: true })
  html?: string;

  @Column("varchar", { nullable: true })
  adLink?: string;

  @Column("boolean", { nullable: true })
  loggedIn?: boolean;

  @Column("varchar", { nullable: true })
  seenOn?: string;
}
